import os
import spacy
import chromadb
from chromadb.utils import embedding_functions
from neo4j import GraphDatabase
import pyodbc
import requests
import json

print("=" * 60)
print("🚀 GraphRAG: COMPLETE INTEGRATION SYSTEM")
print("=" * 60)

# =============================================================================
# CONFIGURATION
# =============================================================================
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

SQL_SERVER = "UCHIHA\\SQLEXPRESS"
SQL_DATABASE = "GraphRAG_DB"

CHROMA_PATH = "./chroma_db"
DOCS_FOLDER = "documents"

# =============================================================================
# STEP 0: INITIALIZE ALL CONNECTIONS
# =============================================================================
print("\n⏳ Initializing connections...")

# spaCy
print("   Loading spaCy...")
nlp = spacy.load("en_core_web_sm")

# Neo4j
print("   Connecting to Neo4j...")
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# ChromaDB
print("   Connecting to ChromaDB...")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_func = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_func
)

# SQL Server
print("   Connecting to SQL Server...")
sql_conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={SQL_SERVER};'
    f'DATABASE={SQL_DATABASE};'
    f'Trusted_Connection=yes;'
)

print("✅ All systems connected!")

# =============================================================================
# STEP 1: LOAD DOCUMENTS
# =============================================================================
def load_documents():
    """Load all .txt files from documents folder"""
    print(f"\n📂 STEP 1: Loading documents from '{DOCS_FOLDER}/'...")
    documents = []
    full_path = os.path.join(os.path.dirname(__file__), DOCS_FOLDER)
    
    for filename in os.listdir(full_path):
        if filename.endswith(".txt"):
            with open(os.path.join(full_path, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            documents.append({"id": filename, "content": content})
            print(f"   ✅ Loaded: {filename}")
    
    print(f"📁 Total: {len(documents)} document(s)")
    return documents

# =============================================================================
# STEP 2: EXTRACT ENTITIES → NEO4J
# =============================================================================
def extract_and_store_entities(doc):
    """Extract entities with spaCy and save to Neo4j"""
    print(f"\n🔍 STEP 2: Extracting entities from {doc['id']}...")
    doc_nlp = nlp(doc["content"])
    entities = []
    
    for ent in doc_nlp.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "DATE"]:
            entities.append({"text": ent.text, "type": ent.label_})
            print(f"   🔍 {ent.text} -> {ent.label_}")
    
    # Store in Neo4j
    with neo4j_driver.session() as session:
        for ent in entities:
            session.run("""
                MERGE (e:Entity {name: $name})
                SET e.type = $type, e.source = $doc_id
            """, name=ent["text"], type=ent["type"], doc_id=doc["id"])
    
    print(f"✅ Stored {len(entities)} entities in Neo4j")
    return entities

# =============================================================================
# STEP 3: BUILD RELATIONSHIPS → NEO4J
# =============================================================================
def build_and_store_relationships(doc):
    """Extract relationships and save to Neo4j"""
    print(f"\n🔗 STEP 3: Building relationships for {doc['id']}...")
    doc_nlp = nlp(doc["content"])
    relationships = []
    
    for sent in doc_nlp.sents:
        ents = [e for e in sent.ents if e.label_ in ["PERSON", "ORG", "GPE", "PRODUCT"]]
        if len(ents) >= 2:
            for i in range(1, len(ents)):
                relationships.append({
                    "source": ents[0].text,
                    "target": ents[i].text,
                    "context": sent.text.strip()
                })
                print(f"   🔗 {ents[0].text} → {ents[i].text}")
    
    # Store in Neo4j
    with neo4j_driver.session() as session:
        for rel in relationships:
            session.run("""
                MATCH (a:Entity {name: $source})
                MATCH (b:Entity {name: $target})
                MERGE (a)-[r:RELATED_TO]->(b)
                SET r.context = $context
            """, source=rel["source"], target=rel["target"], context=rel["context"])
    
    print(f"✅ Stored {len(relationships)} relationships in Neo4j")
    return relationships

# =============================================================================
# STEP 4: STORE IN VECTOR DB (CHROMADB)
# =============================================================================
def store_in_vector_db(doc):
    """Split into chunks and store in ChromaDB"""
    print(f"\n📊 STEP 4: Storing {doc['id']} in ChromaDB...")
    sentences = [s.strip() for s in doc["content"].split('.') if s.strip()]
    
    ids = [f"{doc['id']}_chunk_{i}" for i in range(len(sentences))]
    collection.add(
        documents=sentences,
        ids=ids,
        metadatas=[{"source": doc["id"]} for _ in sentences]
    )
    
    print(f"✅ Stored {len(sentences)} chunks in ChromaDB")
    return len(sentences)

# =============================================================================
# STEP 5: SAVE METADATA → SQL SERVER
# =============================================================================
def save_to_sql(doc_id, title, entity_count, rel_count):
    """Save document metadata to SQL Server"""
    print(f"\n💾 STEP 5: Saving metadata to SQL Server...")
    cursor = sql_conn.cursor()
    
    cursor.execute("""
        IF EXISTS (SELECT 1 FROM Documents WHERE doc_id = ?)
            UPDATE Documents 
            SET entity_count = ?, relationship_count = ?, processed_date = GETDATE()
            WHERE doc_id = ?
        ELSE
            INSERT INTO Documents (doc_id, title, source_path, entity_count, relationship_count)
            VALUES (?, ?, ?, ?, ?)
    """, (doc_id, entity_count, rel_count, doc_id, doc_id, title, 
          f"./documents/{doc_id}", entity_count, rel_count))
    
    sql_conn.commit()
    print(f"✅ Metadata saved to SQL Server")

# =============================================================================
# STEP 6: GRAPH RAG ANSWER ENGINE
# =============================================================================
def answer_question(question):
    """Full GraphRAG pipeline to answer a question"""
    print("\n" + "=" * 60)
    print(f"❓ QUESTION: {question}")
    print("=" * 60)
    
    # 6A: Vector Search
    print("\n🔍 [Step A] Vector Search...")
    vector_results = collection.query(query_texts=[question], n_results=2)
    chunks = vector_results['documents'][0]
    for i, chunk in enumerate(chunks):
        print(f"   📄 {i+1}. {chunk[:80]}...")
    
    # 6B: Graph Search
    print("\n🕸️ [Step B] Graph Search...")
    common = ["Elon Musk", "Tesla", "SpaceX", "Martin Eberhard", 
              "Marc Tarpenning", "Maxwell Technologies"]
    found = [e for e in common if e.lower() in question.lower()]
    
    graph_data = []
    with neo4j_driver.session() as session:
        for entity in found:
            result = session.run("""
                MATCH (e:Entity {name: $name})-[r]-(c)
                RETURN e.name as source, type(r) as relation, c.name as target
                LIMIT 3
            """, name=entity)
            for record in result:
                graph_data.append(dict(record))
                print(f"   🔗 {record['source']} → {record['target']}")
    
    # 6C: LLM Answer
    print("\n🤖 [Step C] Generating answer...")
    prompt = f"""Answer using ONLY this context:

TEXT CONTEXT:
{chr(10).join(chunks)}

GRAPH CONNECTIONS:
{json.dumps(graph_data, indent=2)}

QUESTION: {question}
ANSWER:"""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False}
        )
        answer = response.json()['response']
    except Exception as e:
        answer = f"(LLM not available. From context: {chunks[0] if chunks else 'No info'})"
    
    print(f"\n{'='*60}")
    print(f"✅ ANSWER: {answer}")
    print(f"{'='*60}")
    return answer

# =============================================================================
# MAIN PIPELINE
# =============================================================================
def run_pipeline():
    """Run the complete GraphRAG pipeline"""
    
    # Clear old data for fresh start
    print("\n🧹 Clearing old Neo4j data...")
    with neo4j_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    # Load documents
    docs = load_documents()
    
    # Process each document
    for doc in docs:
        print(f"\n{'#'*60}")
        print(f"📄 PROCESSING: {doc['id']}")
        print(f"{'#'*60}")
        
        entities = extract_and_store_entities(doc)
        relationships = build_and_store_relationships(doc)
        chunks = store_in_vector_db(doc)
        save_to_sql(doc["id"], doc["id"].replace(".txt", "").title(), 
                   len(entities), len(relationships))
    
    # Show final summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    
    with neo4j_driver.session() as session:
        node_count = session.run("MATCH (n) RETURN count(n) as c").single()["c"]
        rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as c").single()["c"]
        print(f"🕸️  Neo4j: {node_count} entities, {rel_count} relationships")
    
    print(f"📊 ChromaDB: {collection.count()} text chunks stored")
    
    cursor = sql_conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Documents")
    sql_count = cursor.fetchone()[0]
    print(f"💾 SQL Server: {sql_count} documents tracked")
    
    # Test questions
    print("\n" + "=" * 60)
    print("🧪 TESTING GRAPH RAG")
    print("=" * 60)
    
    answer_question("Who founded Tesla?")
    answer_question("What companies is Elon Musk connected to?")
    
    print("\n🎉 GraphRAG Pipeline Complete!")

if __name__ == "__main__":
    run_pipeline()