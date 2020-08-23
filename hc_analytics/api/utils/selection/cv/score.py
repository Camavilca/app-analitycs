import json
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from .....db.init import connect_database
from pprint import pprint
from pymongo.errors import ConnectionFailure

FACTOR = 2.85596418997629

def Puntaje_1_CV(data, diccionario):
    PuntTot = sum(diccionario["puntaje"])

    MEAN = diccionario['puntaje'].mean()

    diccionario = diccionario.to_dict()
    PALABRA_CLAVE = diccionario["palabras"]
    PUNTAJE = diccionario["puntaje"]
    N_dic = list(range(0, len(PUNTAJE)))
    base = data["words"][0].split(",")
    puntt = []

    if MEAN == 1:
        for n in N_dic:
            if PALABRA_CLAVE[int(n)] in base:
                puntt.append(PUNTAJE[int(n)])
            else:
                puntt.append(0)
        puntt = round((sum(puntt)/PuntTot),4) * FACTOR
        if puntt >= 0.95:
            puntt = 0.95
            return puntt
        else:
            puntt = round(puntt,4)
            return puntt

    else:
        for n in N_dic:
            if PALABRA_CLAVE[int(n)] in base:
                puntt.append(PUNTAJE[int(n)])
            else:
                puntt.append(0)
        puntt = round((sum(puntt) / PuntTot), 4)
        return puntt


def get_score(ID_CV):
    db = connect_database()
    collection_diccionario = db["keywords"]
    TOTAL_DICCIONARIOS = pd.DataFrame(list(collection_diccionario.find()))
    CV = pd.DataFrame(list(db.cvs.find({"_id": ObjectId(ID_CV)})))

    Puntajes_diccionarios = []
    for i in list(range(0, int(len(TOTAL_DICCIONARIOS)))):
        UN_DICCIONARIO = TOTAL_DICCIONARIOS.iloc[i, 1]
        UN_DICCIONARIO = pd.DataFrame(UN_DICCIONARIO, columns=["palabras", "puntaje"])
        UN_DICCIONARIO["puntaje"] = pd.to_numeric(UN_DICCIONARIO["puntaje"])
        Puntajes_diccionarios.append(Puntaje_1_CV(CV, UN_DICCIONARIO))
    df2 = pd.DataFrame(Puntajes_diccionarios)
    df = TOTAL_DICCIONARIOS["_id"]
    data_final = pd.concat([df, df2], axis=1)
    data_final.columns = ["_id", "puntaje"]

    dictionary = {}
    for index, row in list(data_final.iterrows()):
        dictionary[str(row._id)] = row.puntaje
    print("dictionary", dictionary)
    return dictionary

