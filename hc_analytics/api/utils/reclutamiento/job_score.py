import json
from nltk.corpus import stopwords
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("stopwords")


def get_score(job_description, dictionaries):

    WORD_SCORE = 1
    score_dictionaries = {}

    stopwordsEs = set(stopwords.words("spanish"))

    for dictionary in dictionaries:
        keywords = dictionary["keywords"].split()
        keywordsLength = len(keywords)

        # Acentos a reemplazar
        CAMBIO_ACENTOS = str.maketrans(
            "áéíóúÁÉÍÓÚàèìòùÀÈÌÒÙ", "aeiouAEIOUaeiouAEIOU")

        # Descripcion (input) a analizar
        job_description = (
            str(job_description)
            .replace("#", " ")
            .replace("°", " ")
            .replace("?", "")
            .replace("¿", "")
            .replace("!", "")
            .replace("¡", "")
            .replace("-", "")
            .replace(",", " ")
            .replace("'", "")
            .replace('"', "")
            .replace("–", "")
            .replace("%", "")
            .lower()
            .translate(CAMBIO_ACENTOS)
        )

        # Eliminar stopwords
        words_description = [w for w in job_description.split()]
        for word in words_description:
            if word in stopwordsEs:
                words_description.remove(word)

        # Dar puntuacion
        id = dictionary["_id"]
        score_dictionaries[id] = 0
        for word in keywords:
            if word in words_description:
                score_dictionaries[id] += WORD_SCORE

        score_dictionaries[id] = score_dictionaries[id] / keywordsLength

    return score_dictionaries
