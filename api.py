from flask_restful import Resource
from datetime import datetime
import collections, functools, operator


from db import mongo


collection = mongo.db.data
epoch = datetime.fromtimestamp
        

class TopWords(Resource):
    def get(self):
        result = collection.aggregate([
            {"$project": {"text": {"$split": ["$text", " "]}}},
            {"$unwind": "$text"},
            {"$group": {"_id": "$text", "count": {"$sum": 1}}},
            {"$sort" : { "count" : -1}}
        ])
        response = [{dict(r).get("_id"): dict(r).get("count")} for r in result]

        return {"topwords": response}

class Users(Resource):
    def get(self):
        result = collection.aggregate([
            {"$group": {"_id": "$fromuser", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ])
        response = [{dict(r).get("_id"): dict(r).get("count")} for r in result]
        
        return {"users": response}

class Mentions(Resource):
    def get(self):
        result = collection.aggregate([
            {"$group": {"_id": "$mentions", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ])
        response = [{str(dict(r).get("_id")): dict(r).get("count")} for r in result]

        return {"mentions": response}

class Hourly(Resource):
    def get(self):
        date = collection.distinct("createdat")
        time = [epoch(int(i)).hour for i in date]
        result = collection.aggregate([
            {"$group": {"_id": "$createdat", "text":{'$sum': 1} }},
        ])
        final = [{str(t): dict(r)['text']} for t,r in zip(time,result)]
        response = dict(functools.reduce(operator.add, map(collections.Counter, final))) 
        sortdict = collections.OrderedDict(sorted(response.items()))
        responsef = [{k: v} for k,v in sortdict.items()]

        return {'hourly': responsef}