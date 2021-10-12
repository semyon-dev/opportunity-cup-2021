import datetime

import pymongo
import certifi
import os
from dotenv import load_dotenv
import csv

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

if __name__ == '__main__':

    with open('data.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            # id, Начало, Длительность, Окончание, Последователи, Предшественники
            date_start = str.split(row[1], " ")
            date_end = str.split(row[3], " ")
            hour_minute_start = str.split(date_start[3], ":")
            hour_minute_end = str.split(date_end[3], ":")
            if "," in row[2]:
                duration_array = str.split(row[2], ",")
                duration = int(duration_array[0])
            else:
                duration = int((row[2])[0:-1])

            followers = str.split(row[4], ";"),
            predecessors = str.split(row[5], ";"),
            for elem in followers:
                for i in range(len(elem)):
                    if elem[i].isdigit():
                        continue
                    else:
                        print(elem[i])

            for elem in predecessors:
                for i in range(len(elem)):
                    if elem[i].isdigit():
                        continue
                    else:
                        print(elem[i])

            item = {
                "_id": int(row[0]),
                "start": datetime.datetime(int(date_start[2]), month_to_number[date_start[1]], int(date_start[0]),
                                           int(hour_minute_start[0]),
                                           int(hour_minute_start[1])),
                "duration": duration,
                "end": datetime.datetime(int(date_end[2]), month_to_number[date_end[1]], int(date_end[0]),
                                         int(hour_minute_end[0]),
                                         int(hour_minute_end[1])),
                "followers": str.split(row[4], ";"),
                "predecessors": str.split(row[5], ";")
            }
            # insert_doc(item)
            if line_count % 50 == 0:
                print("line: ", line_count)
                break
            line_count += 1

    print(f'Processed {line_count} lines.')
