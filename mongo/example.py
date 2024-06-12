from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "hr_system"
COLLECTION_NAME = "users"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
users_collection = db[COLLECTION_NAME]


def get_resume_of_user(user_login):
    user = users_collection.find_one({"login": user_login}, {"resume": 1, "_id": 0})
    return user.get("resume", None) if user else None


def get_hobbies_of_user(user_login):
    user = users_collection.find_one({"login": user_login}, {"resume.hobbies": 1, "_id": 0})
    return user.get("resume", {}).get("hobbies", []) if user else []


def get_all_hobbies():
    hobbies = users_collection.distinct("resume.hobbies")
    return hobbies


def get_all_cities():
    cities = users_collection.distinct("resume.previous_jobs.city")
    return cities


def get_hobbies_by_city(city_name):
    users = users_collection.find({"resume.previous_jobs.city": city_name},
                                  {"resume.hobbies": 1, "_id": 0})
    hobbies = set()
    for user in users:
        hobbies.update(user.get("resume", {}).get("hobbies", []))
    return list(hobbies)


def get_users_by_institution():
    pipeline = [
        {"$unwind": "$resume.previous_jobs"},
        {"$group": {
            "_id": "$resume.previous_jobs.institution_name",
            "users": {"$addToSet": "$login"},
            "count": {"$sum": 1}
        }},
        {"$match": {"count": {"$gt": 1}}},
        {"$project": {"institution_name": "$_id", "users": 1, "_id": 0}}
    ]
    return list(users_collection.aggregate(pipeline))


if __name__ == "__main__":
    user_login = "qbaker"
    city_name = "Smithburgh"

    # 1. Забрати рюзюме конкретного працівника
    resume = get_resume_of_user(user_login)
    print(f"Resume of user {user_login}: {resume}\n")

    # 2. Забрати всі хоббі які існують в резюме конкретного працівника
    hobbies_of_user = get_hobbies_of_user(user_login)
    print(f"Hobbies in resume of user {user_login}: {hobbies_of_user}\n")

    # 3. Забрати всі хоббі які існують в резюме усіх працівників
    all_hobbies = get_all_hobbies()
    print(f"All hobbies in resumes of all users: {all_hobbies}\n")

    # 4. Забрати всі міста, що зустрічаються в резюме усіх працівників
    all_cities = get_all_cities()
    print(f"All cities in resumes of all users: {all_cities}\n")

    # 5. Забрати хоббі всіх працівників, що працювали в заданому місті
    hobbies_by_city = get_hobbies_by_city(city_name)
    print(f"Hobbies of users who worked in {city_name}: {hobbies_by_city}\n")

    # 6. Забрати всіх працівників, що працювали в одному закладі (заклад ми не вказуємо)
    users_by_institution = get_users_by_institution()
    print(f"Users who worked in the same institution: "
          f"{set([user for institution_data in users_by_institution for user in institution_data['users']])}")

    client.close()
