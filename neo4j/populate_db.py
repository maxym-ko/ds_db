import sys
sys.path.append('../')

from generate_fake_data import generate_fake_data
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"


class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_data(self, data):
        with self.driver.session() as session:
            for user_data in data:
                session.write_transaction(self.create_user,
                                          user_data['login'],
                                          user_data['password'],
                                          user_data['resume']['resume_title'],
                                          user_data['resume']['hobbies'],
                                          user_data['resume']['previous_jobs'])

        with self.driver.session() as session:
            session.read_transaction(self.print_users)

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

    @staticmethod
    def print_users(tx):
        query = """
        MATCH (u:User)-[:HAS_RESUME]->(r:Resume)
        RETURN u
        """
        result = tx.run(query)
        for record in result:
            print(f"ID: {record['u']['login']}, Login: {record['u']['login']}, Password: {record['u']['password']}")


if __name__ == "__main__":
    client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    fake_data = generate_fake_data()
    client.create_data(fake_data)

    client.close()
