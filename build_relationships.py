import spacy
from neo4j import GraphDatabase
import os

# Load spaCy
print("⏳ Loading spaCy...")
nlp = spacy.load("en_core_web_sm")
print("✅ spaCy ready!")

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

def load_documents(folder_path="documents"):
    """Load all .txt files"""
    documents = []
    full_path = os.path.join(os.path.dirname(__file__), folder_path)
    for filename in os.listdir(full_path):
        if filename.endswith(".txt"):
            with open(os.path.join(full_path, filename), 'r', encoding='utf-8') as f:
                documents.append({"id": filename, "content": f.read()})
    return documents

def extract_relationships(text):
    """
    Find relationships between entities in each sentence.
    Simple rule: If a sentence has 2+ entities, connect them.
    """
    doc = nlp(text)
    relationships = []
    
    for sent in doc.sents:
        # Find all entities in this sentence
        ents = [e for e in sent.ents if e.label_ in ["PERSON", "ORG", "GPE", "PRODUCT"]]
        
        if len(ents) >= 2:
            # Connect first entity to all others in the sentence
            for i in range(1, len(ents)):
                relationships.append({
                    "source": ents[0].text,
                    "target": ents[i].text,
                    "context": sent.text.strip()
                })
                print(f"   🔗 {ents[0].text} → {ents[i].text}")
    
    return relationships

def store_relationships(relationships):
    """Save relationships to Neo4j"""
    with driver.session() as session:
        for rel in relationships:
            session.run("""
                MATCH (a:Entity {name: $source})
                MATCH (b:Entity {name: $target})
                MERGE (a)-[r:RELATED_TO]->(b)
                SET r.context = $context
            """, source=rel["source"], target=rel["target"], context=rel["context"])

def main():
    print("📂 Loading documents...")
    docs = load_documents()
    
    for doc in docs:
        print(f"\n🔎 Processing: {doc['id']}")
        print("-" * 50)
        
        rels = extract_relationships(doc["content"])
        store_relationships(rels)
        
        print(f"✅ Stored {len(rels)} relationships")
    
    print("\n🎉 Done! Open Neo4j Browser and run: MATCH (n)-[r]-(m) RETURN n, r, m")

if __name__ == "__main__":
    main()