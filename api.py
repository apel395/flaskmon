from flask_restful import Resource
from bson.json_util import dumps

from db import mongo


collection = mongo.db.data

class TopWords(Resource):
    def get(self):
        result = collection.aggregate([
            {"$match": {"text": {"$not": {"$size": 1}}}},
            {"$group": {"_id": "$text","count": { "$sum": 1}}},
            {"$match": {"count": { "$gte": 1 }}},
            { "$sort" : { "count" : -1}}
        ])

        response = [dumps(value.values()) for value in result]
        
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
