from neo4j import GraphDatabase

# Replace with your actual Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"


class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_resume_of_user(self, user_login):
        query = """
        MATCH (u:User {login: $login})-[:HAS_RESUME]->(r:Resume)
        RETURN r
        """
        with self.driver.session() as session:
            result = session.run(query, login=user_login)
            return result.single()[0]

    def get_hobbies_of_user(self, user_login):
        query = """
        MATCH (u:User {login: $login})-[:HAS_RESUME]->(r:Resume)-[:HAS_HOBBY]->(h:Hobby)
        RETURN h.name AS hobby
        """
        with self.driver.session() as session:
            result = session.run(query, login=user_login)
            return [record["hobby"] for record in result]

    def get_all_hobbies(self):
        query = """
        MATCH (h:Hobby)
        RETURN DISTINCT h.name AS hobby
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [record["hobby"] for record in result]

    def get_all_cities(self):
        query = """
        MATCH (j:PreviousJob)
        RETURN DISTINCT j.city AS city
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [record["city"] for record in result]

    def get_hobbies_by_city(self, city_name):
        query = """
        MATCH (j:PreviousJob {city: $city})<-[:HAS_PREVIOUS_JOB]-(r:Resume)-[:HAS_HOBBY]->(h:Hobby)
        RETURN DISTINCT h.name AS hobby
        """
        with self.driver.session() as session:
            result = session.run(query, city=city_name)
            return [record["hobby"] for record in result]

    def get_users_by_institution(self):
        query = """
        MATCH (j:PreviousJob)<-[:HAS_PREVIOUS_JOB]-(r:Resume)<-[:HAS_RESUME]-(u:User)
        WITH j.institution_name AS institution, collect(u.login) AS users, count(u) AS user_count
        WHERE user_count > 1
        RETURN institution, users
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [{"institution": record["institution"], "users": record["users"]} for record in result]


if __name__ == "__main__":
    client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    user_login = "qbaker"
    city_name = "Smithburgh"

    # 1. Get resume of a specific user
    resume = client.get_resume_of_user(user_login)
    print(f"Resume of user {user_login}: {resume}\n")

    # 2. Get all hobbies in the resume of a specific user
    hobbies_of_user = client.get_hobbies_of_user(user_login)
    print(f"Hobbies in resume of user {user_login}: {hobbies_of_user}\n")

    # 3. Get all hobbies in the resumes of all users
    all_hobbies = client.get_all_hobbies()
    print(f"All hobbies in resumes of all users: {all_hobbies}\n")

    # 4. Get all cities in the resumes of all users
    all_cities = client.get_all_cities()
    print(f"All cities in resumes of all users: {all_cities}\n")

    # 5. Get hobbies of all users who have worked in a specified city
    hobbies_by_city = client.get_hobbies_by_city(city_name)
    print(f"Hobbies of users who worked in {city_name}: {hobbies_by_city}\n")

    # 6. Get all users who have worked in the same institution
    users_by_institution = client.get_users_by_institution()
    print(f"Users who worked in the same institution: "
          f"{set([user for institution_data in users_by_institution for user in institution_data['users']])}")

    client.close()
