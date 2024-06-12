from neo4j import GraphDatabase
from faker import Faker

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"


class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_data(self):
        faker = Faker()
        hobbies_list = [faker.word() for _ in range(20)]

        with self.driver.session() as session:
            for _ in range(100):
                user_login = faker.user_name()
                user_password = faker.password()
                resume_title = faker.job()
                hobbies = faker.random_choices(elements=hobbies_list, length=5)
                previous_jobs = [
                    {"city": faker.city(), "institution_name": faker.company()}
                    for _ in range(4)
                ]

                session.write_transaction(self.create_user, user_login, user_password, resume_title, hobbies, previous_jobs)

    @staticmethod
    def create_user(tx, login, password, resume_title, hobbies, previous_jobs):
        create_user_query = """
        CREATE (u:User {login: $login, password: $password})
        CREATE (r:Resume {title: $resume_title})
        CREATE (u)-[:HAS_RESUME]->(r)
        """
        tx.run(create_user_query, login=login, password=password, resume_title=resume_title)

        for hobby in hobbies:
            create_hobby_query = """
            MERGE (h:Hobby {name: $hobby_name})
            WITH h
            MATCH (u:User {login: $login})
            MATCH (u)-[:HAS_RESUME]->(r:Resume)
            MERGE (r)-[:HAS_HOBBY]->(h)
            """
            tx.run(create_hobby_query, hobby_name=hobby, login=login)

        for job in previous_jobs:
            create_job_query = """
            CREATE (j:PreviousJob {city: $city, institution_name: $institution_name})
            WITH j
            MATCH (u:User {login: $login})
            MATCH (u)-[:HAS_RESUME]->(r:Resume)
            CREATE (r)-[:HAS_PREVIOUS_JOB]->(j)
            """
            tx.run(create_job_query, city=job['city'], institution_name=job['institution_name'], login=login)


if __name__ == "__main__":
    client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    client.create_data()
    client.close()
