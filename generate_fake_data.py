from faker import Faker
import json


def generate_fake_data():
    faker = Faker()
    faker.seed_instance(0)
    data = []

    hobbies_list = [faker.word() for _ in range(20)]

    for _ in range(100):
        user_data = {
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
        data.append(user_data)

    return data
