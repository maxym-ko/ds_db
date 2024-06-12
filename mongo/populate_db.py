from pymongo import MongoClient
from faker import Faker

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "hr_system"
COLLECTION_NAME = "users"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
users_collection = db[COLLECTION_NAME]

faker = Faker()

# Create some fake data
hobbies_list = [faker.word() for _ in range(20)]

for _ in range(100):
    user = {
        "login": faker.user_name(),
        "password": faker.password(),
        "resume": {
            "resume_title": faker.job(),
            "hobbies": faker.random_choices(elements=hobbies_list, length=5),
            "previous_jobs": [
                {
                    "city": faker.city(),
                    "institution_name": faker.company()
                }
                for _ in range(4)
            ]
        }
    }
    users_collection.insert_one(user)

for user in users_collection.find():
    print(user)

client.close()
