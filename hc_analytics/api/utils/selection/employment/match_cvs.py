import json
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from .....db.init import connect_database

FACTOR = 2.85596418997629

def PuntajeCVCondicionado(data, diccionario):
    N_row = list(range(0,len(data)))
    PuntTot = sum(diccionario['puntaje'])
    
    MEAN = diccionario['puntaje'].mean()

    diccionario = diccionario.to_dict()
    PALABRA_CLAVE = diccionario['palabras']
    PUNTAJE = diccionario['puntaje']

    N_dic = list(range(0,len(PUNTAJE)))
    
    puntuacion_total = []

    for fila in N_row:
        base = data["words"][fila].split(",")

        puntt=[]

        if MEAN == 1:
            # print('reajuste')

            for n in N_dic:
                if PALABRA_CLAVE[int(n)] in base:
                    puntt.append(PUNTAJE[int(n)])
                else:
                    puntt.append(0)
            puntt = round((sum(puntt)/PuntTot),4) * FACTOR
            if puntt >= 0.95:
                puntt = 0.95
                puntuacion_total.append(puntt)
            else:
                puntuacion_total.append(round(puntt,4))

        else:
            for n in N_dic:
                if PALABRA_CLAVE[int(n)] in base:
                    puntt.append(PUNTAJE[int(n)])
                else:
                    puntt.append(0)
            puntt = round((sum(puntt)/PuntTot),4)
            puntuacion_total.append(puntt)
    
    return(puntuacion_total)


def match_cvs(dictionary_id):
    db = connect_database()
    collection_diccionario = db["keywords"]
    print(collection_diccionario)
    CVS = pd.DataFrame(list(db.cvs.find()))

    DICCIONARIO = pd.DataFrame(
        list(collection_diccionario.find({"_id": ObjectId(dictionary_id)}))
    )
    UN_DICCIONARIO = DICCIONARIO["keywords"][0]
    UN_DICCIONARIO = pd.DataFrame(UN_DICCIONARIO, columns=["palabras", "puntaje"])
    UN_DICCIONARIO["puntaje"] = pd.to_numeric(UN_DICCIONARIO["puntaje"])
    df2 = PuntajeCVCondicionado(CVS, UN_DICCIONARIO)
    df2 = pd.DataFrame(df2, columns=["Match"])
    df1 = CVS["_id"]
    df = pd.concat([df1, df2], axis=1)
    json = {}
    for index, row in list(df.iterrows()):
        json[str(row._id)] = row.Match
    return json
