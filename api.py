from flask_restful import Resource
from datetime import datetime


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
        text = collection.distinct("text")

        time = [epoch(int(i)).hour for i in date]

        result = collection.aggregate([
            # {"$project": {"createdat": {"$toDate": "$createdat"}}},
            # {'$match': {'createdat': {'$lte': "ISODate('1371324588')", '$gte': "ISODate('1371311470')"}}},
            {"$group": {"_id": "$text", "createdat":{'$sum': 1} }},
            {"$sort": {"createdat": -1}},
            # {"$project": {"createdat": 0}}
        ])
        
        # print(type(result))
        return [{str(r): t} for r,t in zip(date,time)]
        # return jsonify({str(t): str(r) for t,r in zip(time, result)})