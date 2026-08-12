import spacy
from neo4j import GraphDatabase
import os

# Load spaCy's English model (we installed this in Step 1)
print("⏳ Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")
print("✅ spaCy model loaded!")

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"  # Your password
driver = GraphDatabase.driver(uri, auth=(username, password))

def load_documents(folder_path="documents"):
    """Load all .txt files from the documents folder"""
    documents = []
    full_path = os.path.join(os.path.dirname(__file__), folder_path)
    
    for filename in os.listdir(full_path):
        if filename.endswith(".txt"):
            with open(os.path.join(full_path, filename), 'r', encoding='utf-8') as f:
                documents.append({
                    "id": filename,
                    "content": f.read()
                })
    return documents

def extract_entities(text):
    """
    Use spaCy to find entities in text.
    Returns a list of entities with their type.
    """
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        # We only care about these types:
        if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "DATE"]:
            entities.append({
                "text": ent.text,
                "type": ent.label_
            })
            print(f"   🔍 Found: {ent.text} -> {ent.label_}")
    
    return entities

def store_entities_in_neo4j(doc_id, entities):
    """
    Save extracted entities to Neo4j knowledge graph.
    If entity already exists, it updates it (MERGE).
    """
    with driver.session() as session:
        for ent in entities:
            session.run("""
                MERGE (e:Entity {name: $name})
                SET e.type = $type, e.source = $doc_id
            """, name=ent["text"], type=ent["type"], doc_id=doc_id)

def main():
    print("📂 Loading documents...")
    docs = load_documents()
    print(f"📁 Found {len(docs)} document(s)\n")
    
    for doc in docs:
        print(f"🔎 Processing: {doc['id']}")
        print("-" * 40)
        
        # Extract entities
        entities = extract_entities(doc["content"])
        
        # Store in Neo4j
        store_entities_in_neo4j(doc["id"], entities)
        
        print(f"✅ Stored {len(entities)} entities in Neo4j\n")
    
    print("🎉 All done! Check Neo4j Browser to see your entities.")

if __name__ == "__main__":
    main()