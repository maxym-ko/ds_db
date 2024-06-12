from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"


class Neo4jClient:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clean_db(self):
        with self.driver.session() as session:
            session.write_transaction(self.delete_all)

    @staticmethod
    def delete_all(tx):
        tx.run("MATCH (n) DETACH DELETE n")


if __name__ == "__main__":
    client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    client.clean_db()
    client.close()
