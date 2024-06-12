from faker import Faker
import json


def generate_fake_data():
    faker = Faker()
    faker.seed_instance(0)
    data = []

    hobbies = [
        'Reading', 'Writing', 'Painting', 'Drawing', 'Cooking', 'Baking', 'Gardening',
        'Hiking', 'Running', 'Swimming', 'Cycling', 'Photography', 'Traveling',
        'Playing guitar', 'Playing piano', 'Knitting', 'Sewing', 'Crafting', 'Playing soccer',
        'Playing basketball', 'Playing tennis', 'Bird watching', 'Playing board games',
        'Collecting stamps', 'Collecting coins', 'Fishing', 'Camping', 'Dancing', 'Yoga',
        'Meditation', 'Volunteering', 'Learning new languages', 'Watching movies',
        'Playing video games', 'Doing puzzles', 'Practicing martial arts', 'Woodworking'
    ]
    companies = [faker.company() for _ in range(200)]

    for _ in range(10):
        user_data = {
            "login": faker.user_name(),
            "password": faker.password(),
            "resume": {
                "resume_title": faker.job(),
                "hobbies": faker.random_choices(elements=hobbies, length=3),
                "previous_jobs": [
                    {
                        "city": faker.city(),
                        "institution_name": faker.random_choices(companies)[0]
                    }
                    for _ in range(3)
                ]
            }
        }
        data.append(user_data)

    return data
