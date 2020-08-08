from pymongo import MongoClient
from pandas import DataFrame
from bson import ObjectId

ravi_client = MongoClient(
        "mongodb+srv://projectflask:projectflask@cluster0-eccmq.mongodb.net/admin?retryWrites=true&w=majority")
ravi_db = ravi_client["user_details"]