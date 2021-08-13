import pymongo
from pymongo import MongoClient

import os
from dotenv import load_dotenv
import json

with open("./config.json", "r") as config_file:
    config = json.load(config_file)

load_dotenv()

cluster = MongoClient(os.environ.get("db_string"))

if config["dev_mode"]:
    db = cluster["test_blackjack"]
elif not config["dev_mode"]:
    db = cluster["blackjack"]

collection = db["db"]
