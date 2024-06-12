from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "hr_system"
COLLECTION_NAME = "users"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
users_collection = db[COLLECTION_NAME]

# Delete all documents in the users collection
result = users_collection.delete_many({})

print(f"Deleted {result.deleted_count} documents from the '{COLLECTION_NAME}' collection.")

client.close()
