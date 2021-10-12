import pymongo
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

# Create the database for our example
db = client.main
data_collection = db.data


def insert_doc(doc):
    try:
        data_collection.insert_one(doc)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    item = {
        "id": 1,
        "quantity": 2,
        "ingredients": "all-purpose flour",
        "expiry_date": "expiry"
    }
    insert_doc(item)
