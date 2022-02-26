import pymongo
import os

ip = os.getenv("MONGO_IP", "127.0.0.1")

client = pymongo.MongoClient(ip, 27017)
db = client["database"]
collection = db.collection


def add_object(classification, x_coordinate, y_coordinate, date, file_name):
    post = {
        "classification": classification,
        "x_coordinate": x_coordinate,
        "y_coordinate": y_coordinate,
        "date": date,
        "file_name": file_name,
    }

    db.collection.insert_one(post)


def get_objects_by_date(date):
    field = {"date": date}
    posts = []
    for post in db.collection.find(field):
        posts.append(post)
    
    return posts