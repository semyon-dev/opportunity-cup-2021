import pymongo
import certifi

# Provide the mongodb atlas url to connect python to mongodb using pymongo

CONNECTION_STRING = "mongodb+srv://root:root@cluster0.ik40a.mongodb.net/Cluster0?retryWrites=true&w=majority&tls=true"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

# Create the database for our example (we will use the same database throughout the tutorial
db = client['main']
data_collection = db["data"]


def insert_doc():
    item_3 = {
        "id": 0,
        "quantity": 2,
        "ingredients": "all-purpose flour",
        "expiry_date": "expiry"
    }
    data_collection.insert_one(item_3)
