from flask_restful import Resource
from bson.json_util import dumps

from db import mongo


collection = mongo.db.data

class TopWords(Resource):
    def get(self):
        resp = collection.aggregate([
            {"$match": {
                "text": { "$not": {"$size": 0} }
                }
            },
            {"$unwind": "$text" },
            {"$group": {
                "_id": {"$toLower": "$text"},
                "count": { "$sum": 1 }
                }
            },
            {"$match": {
                "count": { "$gte": 2 }
                }
            },
            { "$sort" : { "count" : -1} },
            { "$limit" : 100 }
        ])

        # field = {"text":1, "_id":0}
        # query = collection.find(
        #     {"$text":{"$search":"makan"}},
        #     field
        # )
        for key in resp:
            dict(key)
            print('{}: {}'.format(key.value, key.value))

        return dumps(resp)

class Users(Resource):
    def get(self):
        result = collection.find({"fromuser": {"$gt": 1}})
        return dumps(result)

class Mentions(Resource):
    def get(self):
        collection.find()

class Hourly(Resource):
    def get(self):
        resp = collection.distinct("text", {"fromuser": "farn_a"})
        return dumps(resp)
