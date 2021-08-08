import pymongo
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

cluster = MongoClient(os.environ.get("db_string"))
db = cluster["blackjack"]
collection = db["db"]
