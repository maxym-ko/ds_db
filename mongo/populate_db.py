import sys
sys.path.append('../')

from generate_fake_data import generate_fake_data
from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "hr_system"
COLLECTION_NAME = "users"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
users_collection = db[COLLECTION_NAME]

fake_data = generate_fake_data()

for user_data in fake_data:
    user_document = {
        "login": user_data["login"],
        "password": user_data["password"],
        "resume": {
            "resume_title": user_data["resume"]["resume_title"],
            "hobbies": user_data["resume"]["hobbies"],
            "previous_jobs": user_data["resume"]["previous_jobs"]
        }
    }
    users_collection.insert_one(user_document)

for user in users_collection.find():
    print(user)

client.close()
