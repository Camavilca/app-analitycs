from pymongo import MongoClient
import ssl
import os


DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")

print("BD_URI", DB_URI)
print("DB_NAME", DB_NAME)


def connect_database():
    client = MongoClient(DB_URI, ssl_cert_reqs=ssl.CERT_NONE)
    return client[DB_NAME]
