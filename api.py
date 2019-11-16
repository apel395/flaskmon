from flask_restful import Resource
from bson.json_util import dumps
from flask import jsonify


from db import mongo


collection = mongo.db.data

class TopWords(Resource):
    def get(self):
        result = collection.aggregate([
            {"$project": {"text": {"$split": ["$text", " "]}}},
            {"$unwind": "$text"},
            {"$group": {"_id": "$text", "count": {"$sum": 1}}},
            { "$sort" : { "text" : -1}}
        ])
        response = [dumps(value.values()) for value in result]
        print(len(response))
        
        return response

class Users(Resource):
    def get(self):
        result = collection.aggregate([
            {'$group': {'_id': '$fromuser', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ])
        response = [dumps(value.values()) for value in result]
        
        return response

class Mentions(Resource):
    def get(self):
        result = collection.aggregate([
            {'$group': {'_id': '$mentions', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}}
        ])
        response = [dumps(value.values()) for value in result]
        
        return response

class Hourly(Resource):
    def get(self):
        resp = collection.distinct("text", {"fromuser": "farn_a"})
        return dumps(resp)
