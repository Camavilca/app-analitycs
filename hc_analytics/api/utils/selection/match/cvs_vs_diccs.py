import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

# pprint library is used to make the output look more pretty
from pprint import pprint

from .....db.init import connect_database

# client = MongoClient('mongodb+srv://Admin:HCP2019@cluster0-zj9i0.mongodb.net/test?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
# # db=client.test
# db=client["test"]

# collection_diccionario=db["keywords"]
# TOTAL_DICCIONARIOS = pd.DataFrame(list(collection_diccionario.find()))


# print(TOTAL_DICCIONARIOS.head())

# CV = pd.DataFrame(list(db.cvs.find()))

FACTOR = 2.85596418997629


def PuntajeCV(data, diccionario):
    N_row = list(range(0, len(data)))
    PuntTot = sum(diccionario["puntaje"])

    MEAN = diccionario["puntaje"].mean()

    diccionario = diccionario.to_dict()
    PALABRA_CLAVE = diccionario["palabras"]
    PUNTAJE = diccionario["puntaje"]

    N_dic = list(range(0, len(PUNTAJE)))

    puntuacion_total = []

    for fila in N_row:

        base = data["words"][fila].split(",")
        puntt = []

        if MEAN == 1:
            for n in N_dic:
                if PALABRA_CLAVE[int(n)] in base:
                    puntt.append(PUNTAJE[int(n)])
                else:
                    puntt.append(0)
            puntt = round((sum(puntt) / PuntTot), 4) * FACTOR
            if puntt >= 0.95:
                puntt = 0.95
                puntuacion_total.append(puntt)
            else:
                puntuacion_total.append(round(puntt, 4))

        else:
            for n in N_dic:
                if PALABRA_CLAVE[int(n)] in base:
                    puntt.append(PUNTAJE[int(n)])
                else:
                    puntt.append(0)
            puntt = round((sum(puntt) / PuntTot), 4)
            puntuacion_total.append(puntt)

    return puntuacion_total


def get_match_all():
    db = connect_database()
    # collection_diccionario = db["keywords"]

    TOTAL_DICCIONARIOS = pd.DataFrame(list(db.keywords.find()))
    CVs = pd.DataFrame(list(db.cvs.find()))

    Puntajes_diccionarios = []
    for i in list(range(0, int(len(TOTAL_DICCIONARIOS)))):
        UN_DICCIONARIO = TOTAL_DICCIONARIOS.iloc[i, 1]
        UN_DICCIONARIO = pd.DataFrame(UN_DICCIONARIO, columns=["palabras", "puntaje"])
        UN_DICCIONARIO["puntaje"] = pd.to_numeric(UN_DICCIONARIO["puntaje"])
        Puntajes_diccionarios.append(PuntajeCV(CVs, UN_DICCIONARIO))
    N_row = len(CVs)
    N_col = len(TOTAL_DICCIONARIOS)
    M = np.array(Puntajes_diccionarios).reshape(
        N_col, N_row
    )  # aqui rellena por columnas por lo que debe transponerse luego
    M = np.transpose(M)
    df = pd.DataFrame(M)  # de lista a dataframe
    # df.columns = nombres_col_diccionarios
    df.columns = TOTAL_DICCIONARIOS["_id"]  # pone el id como nombre de columna
    CVs = CVs["_id"]
    df.index = CVs  # pone el nombre de fila como id de CV
    json_index = df.to_dict(
        orient="index"
    )  # crea un JSON tomando el Id de fila como campo
    result = []
    for cv_id in json_index:
        temp = {}
        temp["cvId"] = str(cv_id)
        temp["dictionaries"] = {}
        for dicc_id in json_index[cv_id]:
            temp["dictionaries"][str(dicc_id)] = json_index[cv_id][dicc_id]
        print("temp", temp)
        result.append(temp)

    # {
    #     "aksjdnsakjdnksajd CVID": {
    #         "ObjectId(laksmdlakmdlak DICC ID)": 0.99,
    #         "laksmdlakmdlak DICC ID": 0.99,
    #         "laksmdlakmdlak DICC ID": 0.99,
    #     }
    # }

    # [
    #     {
    #         "cvId": "dnaskdnslakdnaks",
    #         "dicctionaries": {
    #             "askdnlsdnalklkmdla": 0.88,
    #             "askdnlsdnalklkmdla": 0.88,
    #             "askdnlsdnalklkmdla": 0.88,
    #         }
    #     }
    # ]

    return result
