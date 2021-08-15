import pymongo
from pymongo import MongoClient

import os
from dotenv import load_dotenv
import json

with open("./config.json", "r") as config_file:
    config = json.load(config_file)

load_dotenv()

cluster = MongoClient(os.environ.get("db_string"))

db = cluster["test_blackjack"] if config["dev_mode"] else cluster["blackjack"]
collection = db["db"]
