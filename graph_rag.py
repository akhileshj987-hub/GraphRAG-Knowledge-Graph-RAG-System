from neo4j import GraphDatabase
import chromadb
from chromadb.utils import embedding_functions
import requests
import json

print("🚀 Initializing GraphRAG System...")

class GraphRAG:
    def __init__(self):
        # 1. Connect to Neo4j (Knowledge Graph)
        self.neo4j_driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "12345678")
        )
        
        # 2. Connect to ChromaDB (Vector DB)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_collection(
            name="documents",
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )
        
        print("✅ GraphRAG System Ready!")
        print("   🕸️ Neo4j connected")
        print("   📊 ChromaDB connected")
    
    def vector_search(self, question, n_results=2):
        """Find similar text chunks using vector similarity"""
        print(f"\n🔍 [Step 1] Vector Search: '{question}'")
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        chunks = results['documents'][0]
        for i, chunk in enumerate(chunks):
            print(f"   📄 Result {i+1}: {chunk[:80]}...")
        return chunks
    
    def graph_search(self, question):
        """Find entities and their connections in Neo4j"""
        print(f"\n🕸️ [Step 2] Graph Search: '{question}'")
        
        # Simple: extract potential entity names from question
        # (In production, use NER. Here we check common ones)
        common_entities = ["Elon Musk", "Tesla", "SpaceX", "Martin Eberhard", 
                          "Marc Tarpenning", "Maxwell Technologies"]
        found_entities = [e for e in common_entities if e.lower() in question.lower()]
        
        connections = []
        with self.neo4j_driver.session() as session:
            for entity in found_entities:
                result = session.run("""
                    MATCH (e:Entity {name: $name})-[r]-(connected)
                    RETURN e.name as source, type(r) as relation, 
                           connected.name as target
                    LIMIT 5
                """, name=entity)
                for record in result:
                    connections.append(dict(record))
                    print(f"   🔗 {record['source']} → {record['target']}")
        
        return connections
    
    def ask_llm(self, question, vector_context, graph_context):
        """Use Ollama LLM to generate final answer"""
        print(f"\n🤖 [Step 3] Generating answer with LLM...")
        
        prompt = f"""You are a helpful assistant. Use ONLY the provided context to answer the question.
If the context doesn't have the answer, say "I don't have enough information."

--- VECTOR SEARCH CONTEXT (Similar text chunks) ---
{chr(10).join(vector_context)}

--- GRAPH CONTEXT (Connected entities) ---
{json.dumps(graph_context, indent=2)}

--- QUESTION ---
{question}

--- ANSWER ---
"""
        
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                }
            )
            answer = response.json()['response']
            return answer
        except Exception as e:
            return f"⚠️ Ollama error: {e}\n\n(Quick answer from context: {vector_context[0] if vector_context else 'No info'})"
    
    def answer(self, question):
        """Main method: Run full GraphRAG pipeline"""
        print("=" * 60)
        print(f"❓ QUESTION: {question}")
        print("=" * 60)
        
        # Step 1: Vector search
        vector_results = self.vector_search(question)
        
        # Step 2: Graph search
        graph_results = self.graph_search(question)
        
        # Step 3: LLM answer
        answer = self.ask_llm(question, vector_results, graph_results)
        
        print("\n" + "=" * 60)
        print(f"✅ ANSWER: {answer}")
        print("=" * 60)
        return answer

# Run tests
if __name__ == "__main__":
    rag = GraphRAG()
    
    # Test Question 1
    rag.answer("Who founded Tesla?")
    
    print("\n" + "-" * 60 + "\n")
    
    # Test Question 2
    rag.answer("What companies is Elon Musk connected to?")