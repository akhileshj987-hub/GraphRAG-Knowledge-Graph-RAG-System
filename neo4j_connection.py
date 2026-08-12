from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"  # ⚠️ CHANGE THIS to the password you set in Neo4j Desktop

driver = GraphDatabase.driver(uri, auth=(username, password))

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Hello GraphRAG!' as message")
        print(result.single()["message"])

if __name__ == "__main__":
    test_connection()
    print("✅ Connected to Neo4j successfully!")