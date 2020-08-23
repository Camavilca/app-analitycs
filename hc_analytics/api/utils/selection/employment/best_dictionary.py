import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import string
from pymongo.errors import ConnectionFailure
import pprint


import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("stopwords")

from nltk.corpus import stopwords
from string import digits
import re
import pandas as pd
from .....db.init import connect_database
import numpy as np

LIMITE = 95

def get_Description_clean(descripcion):
    descripcion = descripcion.lower().split("requisitos")[1]

    CAMBIO_ACENTOS = str.maketrans("áéíóúÁÉÍÓÚàèìòùÀÈÌÒÙ", "aeiouAEIOUaeiouAEIOU")
    # borrando correos
    subst = "m"
    regex = r"\S*@\S*\s?"
    descripcion = re.sub(regex, subst, descripcion, 0)
    # publicacion_puesto

    ## eliminando numeros
    remove_digits = str.maketrans("", "", digits)
    descripcion = descripcion.translate(remove_digits)

    ## quitar caracteres especiales
    chars = re.escape(string.punctuation)
    descripcion = re.sub(r"[" + chars + "]", " ", descripcion)

    descripcion = (
            str(descripcion)
            .replace("°", ",")
            .replace("•", ",")
            .replace("°", ",")
            .replace("“", ",")
            .replace("”", ",")
            .replace("·", ",")
            .replace(" ", ",")
            .replace("\n", ",")
            .replace("  ", ",")
            .replace(",,,,,,", ",")
            .replace(",,,,,", ",")
            .replace(",,,,", ",")
            .replace(",,,", ",")
            .replace(",,", ",")
            .lower()  # minuscula
            .translate(CAMBIO_ACENTOS)
            .strip()
        )

    STOPW_1 = stopwords.words("spanish")
    S = list()
    for stop in STOPW_1:
        yy = stop.translate(CAMBIO_ACENTOS)
        S.append(yy)
    STOPW_1 = S
    STOPW_2 = list(range(0, 1000, 1))
    STOPW_3 = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "ñ",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "lun",
            "vie",
            "am",
            "año",
            "años",
            "dado",
            "etc",
            "gran",
            "pm",
            "san",
            "isidro",
            "human",
            "planning",
            "capital",
            "traves",
            "hcp",
            "junto",
        "rr","hh",
            "nbsp"
    ]
    STOPWORDS_TOT = STOPW_1 + STOPW_2 + STOPW_3
        # elimina stopwords
    tokens = [t for t in descripcion.split(",")]
    descripcion_limpia = tokens[:]
    for token in tokens:
        if token in STOPWORDS_TOT:
            descripcion_limpia.remove(token)

    # crea el dataframe
    data = {"palabras": descripcion_limpia}
    df = pd.DataFrame(data, columns=["palabras"])
    # elimina duplicados
    df.drop_duplicates("palabras", keep="first", inplace=True)
    # ordena valores
    df = df.sort_values(by="palabras", ascending=True)
    # eliminando celdas vacias
    df["palabras"].replace("", np.nan, inplace=True)
    df.dropna(subset=["palabras"], inplace=True)
    x = df.to_string(header=False, index=False, index_names=False).split("\n")
    vals = [",".join(ele.split()) for ele in x]
    return vals

def get_Dictionary_cte(words_list):
    puntaje = [1] * len(words_list)
    # crea el dataframe
    data = {"palabras": words_list, "puntaje": puntaje}
    df = pd.DataFrame(data, columns=["palabras", "puntaje"])
    # elimina duplicados
    df.drop_duplicates("palabras", keep="first", inplace=True)
    # ordena valores
    df = df.sort_values(by="palabras", ascending=True)
    # eliminando celdas vacias
    df["palabras"].replace("", np.nan, inplace=True)
    df.dropna(subset=["palabras"], inplace=True)
    return df


def Max_Score_Dictionary(tabla):
    base = tabla["puntaje"].argmax()
    base = tabla.iloc[int(base), :]
    return base


def Words_vs_Dictionay(data, diccionario):
    PuntTot = sum(diccionario["puntaje"])
    diccionario = diccionario.to_dict()
    PALABRA_CLAVE = diccionario["palabras"]
    PUNTAJE = diccionario["puntaje"]
    N_dic = list(range(0, len(PUNTAJE)))
    puntt = []
    for n in N_dic:
        if PALABRA_CLAVE[int(n)] in data:
            puntt.append(PUNTAJE[int(n)])
        else:
            puntt.append(0)
    puntt = round((sum(puntt) / PuntTot), 4)
    return puntt


def get_best_dictionary(descripcion):
    db = connect_database()
    collection_diccionario = db["keywords"]
    TOTAL_DICCIONARIOS = pd.DataFrame(
        list(collection_diccionario.find({"type": "AUTOMATIC"}))
    )
    palabras_dicc = get_Description_clean(descripcion)
    Puntajes_diccionarios = []
    for i in list(range(0, int(len(TOTAL_DICCIONARIOS)))):
        UN_DICCIONARIO = TOTAL_DICCIONARIOS.iloc[i, 1]
        UN_DICCIONARIO = pd.DataFrame(UN_DICCIONARIO, columns=["palabras", "puntaje"])
        UN_DICCIONARIO["puntaje"] = pd.to_numeric(UN_DICCIONARIO["puntaje"])
        Puntajes_diccionarios.append(Words_vs_Dictionay(palabras_dicc, UN_DICCIONARIO))
    df2 = pd.DataFrame(Puntajes_diccionarios)
    df = TOTAL_DICCIONARIOS["_id"]
    df_total = pd.concat([df, df2], axis=1)
    df_total.columns = ["_id", "puntaje"]
    Fila_match = Max_Score_Dictionary(df_total)
    if LIMITE < float(Fila_match[1]):
        dic = dict(dicctionaryId=Fila_match[0], additionalWords=None)
        return dic
    else:
        NewDictionary = get_Dictionary_cte(get_Description_clean(descripcion))
        dictionaryArray = []
        for index, row in list(NewDictionary.iterrows()):
            dictionary = {}
            dictionary["words"] = row.palabras
            dictionary["score"] = row.puntaje
            dictionaryArray.append(dictionary)
        dic = dict(dicctionaryId=None, additionalWords=dictionaryArray)
        return dic
    return None

