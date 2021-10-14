import csv
import datetime
import os

import certifi
import flask
import pymongo
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask import request

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

# Create the database for our example
db = client.main
data_collection = db.data

app = Flask(__name__)
CORS(app)


@app.route("/data")
def hello():
    reply = []
    for post in data_collection.find():
        reply.append(post)
    return {'data': reply}


def get_doc(id):
    return data_collection.find_one({'_id': int(id)})


def count(id, count_itog, cost, offset):
    doc = get_doc(id)
    if doc is None:
        return count_itog, cost
    if 'followers' not in doc:
        return count_itog, cost
    for follower in doc['followers']:
        docF = get_doc(follower['n'])
        if 'start' in docF and 'end' in doc:
            buffer = docF['start'] - doc['end']
            buffer_seconds = buffer.total_seconds()
            offset_seconds = offset * 24 * 3600
            if buffer_seconds - offset_seconds < 0:
                # count_itog += 1
                if docF['duration'] == 0:
                    cost += 1000
                    # cost += 1
                count_itog2, cost2 = count(docF['_id'], count_itog, cost,
                                           abs(buffer_seconds - offset_seconds) / 3600 / 24)
                count_itog = count_itog2 + 1
                cost = cost2 + 1
    return count_itog, cost


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return flask.jsonify({"message": "invalid request, check README"})


@app.route("/offset")
def offset():
    id = int(request.args.get('id', 0))
    offset = int(request.args.get('offset', 0))
    countVar, cost = count(id, 0, 0, offset)
    return {"count": countVar, "cost": cost}


if __name__ == "__main__":
    app.run(threaded=True, port=int(os.environ.get('PORT', 5000)))

month_to_number = {
    'Январь': 1,
    'Февраль': 2,
    'Март': 3,
    'Апрель': 4,
    'Май': 5,
    'Июнь': 6,
    'Июль': 7,
    'Август': 8,
    'Сентябрь': 9,
    'Октябрь': 10,
    'Ноябрь': 11,
    'Декабрь': 12
}


def insert_doc(doc):
    try:
        data_collection.insert_one(doc)
    except Exception as e:
        print(e)


def parse_format(items: list):
    arr: list = []
    for elem in items:
        # пропускаем плохие данные
        if ".." in elem:
            continue
        parsed_item: dict = {
            "n": '',
        }
        for e in range(len(elem)):
            if elem[e].isdigit():
                parsed_item["n"] += elem[e]
            else:
                parsed_item["X"] = elem[e]
                parsed_item["Y"] = elem[e + 1]
                if elem[e + 2:] != "":
                    parsed_item["m"] = elem[e + 2:]
                    parsed_item["m"] = str.removesuffix(parsed_item["m"], "д")
                break
        if parsed_item["n"] != '':
            parsed_item["n"] = int(parsed_item["n"])
        arr.append(parsed_item)
    return arr


def parse_file_mongodb():
    with open('data.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            # id, Начало, Длительность, Окончание, Последователи, Предшественники
            item = {
                "_id": int(row[0]),
            }
            if row[1] != "":
                date_start = str.split(row[1], " ")
                hour_minute_start = str.split(date_start[3], ":")
                item["start"] = datetime.datetime(int(date_start[2]), month_to_number[date_start[1]],
                                                  int(date_start[0]),
                                                  int(hour_minute_start[0]),
                                                  int(hour_minute_start[1]))
            if row[2] != "":
                if "," in row[2]:
                    duration_array = str.split(row[2], ",")
                    duration = int(duration_array[0])
                else:
                    duration = int((row[2])[0:-1])
                item["duration"] = duration
            if row[3] != "":
                date_end = str.split(row[3], " ")
                hour_minute_end = str.split(date_end[3], ":")
                item["end"] = datetime.datetime(int(date_end[2]), month_to_number[date_end[1]], int(date_end[0]),
                                                int(hour_minute_end[0]),
                                                int(hour_minute_end[1]))
            if row[4] != "":
                followers_mongo = parse_format(str.split(row[4], ";"))
                item["followers"] = followers_mongo
            if row[5] != "":
                predecessors_mongo = parse_format(str.split(row[5], ";"))
                item["predecessors"] = predecessors_mongo
            # insert_doc(item)
            if line_count % 100 == 0:
                print("line: ", line_count)
            line_count += 1

    print(f'\nProcessed {line_count} lines.')
