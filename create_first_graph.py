from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"  # ✅ Your password
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_knowledge():
    with driver.session() as session:
        # Delete old data (clean slate)
        session.run("MATCH (n) DETACH DELETE n")
        
        # Create person node
        session.run("""
            CREATE (p:Person {name: 'Elon Musk', role: 'CEO'})
        """)
        
        # Create company node
        session.run("""
            CREATE (c:Company {name: 'Tesla', industry: 'Automotive'})
        """)
        
        # Create relationship between them
        session.run("""
            MATCH (p:Person {name: 'Elon Musk'})
            MATCH (c:Company {name: 'Tesla'})
            CREATE (p)-[:WORKS_AS_CEO_OF]->(c)
        """)
        
        print("✅ Knowledge graph created!")

def show_graph():
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN n.name as name, labels(n) as type")
        print("\n📊 Nodes in your graph:")
        for record in result:
            print(f"   {record['name']} -> {record['type']}")

if __name__ == "__main__":
    create_knowledge()
    show_graph()