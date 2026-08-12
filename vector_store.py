import chromadb
from chromadb.utils import embedding_functions
import os

print("⏳ Setting up ChromaDB...")

# Create a folder to store the vector database
client = chromadb.PersistentClient(path="./chroma_db")

# Use a free embedding model (all-MiniLM-L6-v2)
# This converts text into numbers so we can compare similarity
embedding_func = embedding_functions.DefaultEmbeddingFunction()

# Create a collection (like a table in SQL)
collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_func
)

print("✅ ChromaDB ready!")

def load_documents(folder_path="documents"):
    """Load all .txt files"""
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

def store_in_vector_db():
    """Split documents into chunks and store in ChromaDB"""
    docs = load_documents()
    
    for doc in docs:
        # Split by sentences (simple approach)
        sentences = [s.strip() for s in doc["content"].split('.') if s.strip()]
        
        ids = [f"{doc['id']}_chunk_{i}" for i in range(len(sentences))]
        
        collection.add(
            documents=sentences,
            ids=ids,
            metadatas=[{"source": doc["id"]} for _ in sentences]
        )
        
        print(f"✅ Stored {len(sentences)} chunks from {doc['id']}")

def test_vector_search():
    """Test: Ask a question and find similar text"""
    print("\n🔍 Testing vector search...")
    
    question = "Who founded Tesla?"
    
    results = collection.query(
        query_texts=[question],
        n_results=2  # Get top 2 matches
    )
    
    print(f"\n❓ Question: {question}")
    print("📄 Most similar text chunks:")
    for i, doc in enumerate(results['documents'][0]):
        print(f"   {i+1}. {doc}")

if __name__ == "__main__":
    store_in_vector_db()
    test_vector_search()