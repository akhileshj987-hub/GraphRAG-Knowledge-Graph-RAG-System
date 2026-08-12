import streamlit as st
import os
import spacy
import chromadb
from chromadb.utils import embedding_functions
from neo4j import GraphDatabase
import pyodbc
import requests
import json

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="GraphRAG System",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ GraphRAG: Knowledge Graph + RAG System")
st.markdown("Ask questions about your documents. The system searches **vector database** + **knowledge graph** + **LLM** to answer.")

# =============================================================================
# INITIALIZE CONNECTIONS (Cached so they don't reload)
# =============================================================================
@st.cache_resource
def init_system():
    """Initialize all connections once"""
    systems = {}
    
    # spaCy
    systems["nlp"] = spacy.load("en_core_web_sm")
    
    # Neo4j
    systems["neo4j"] = GraphDatabase.driver(
        "bolt://localhost:7687", auth=("neo4j", "12345678")
    )
    
    # ChromaDB
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    systems["collection"] = chroma_client.get_collection(
        name="documents",
        embedding_function=embedding_functions.DefaultEmbeddingFunction()
    )
    
    # SQL Server
    systems["sql"] = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER=UCHIHA\\SQLEXPRESS;'
        f'DATABASE=GraphRAG_DB;'
        f'Trusted_Connection=yes;'
    )
    
    return systems

# Load systems
try:
    systems = init_system()
    st.sidebar.success("✅ All systems connected!")
except Exception as e:
    st.sidebar.error(f"❌ Connection failed: {e}")
    st.stop()

# =============================================================================
# SIDEBAR: SYSTEM STATUS
# =============================================================================
st.sidebar.header("📊 System Status")

# Neo4j stats
with systems["neo4j"].session() as session:
    node_count = session.run("MATCH (n) RETURN count(n) as c").single()["c"]
    rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as c").single()["c"]
    st.sidebar.metric("🕸️ Neo4j Entities", node_count)
    st.sidebar.metric("🔗 Neo4j Relations", rel_count)

# ChromaDB stats
st.sidebar.metric("📄 Vector Chunks", systems["collection"].count())

# SQL stats
cursor = systems["sql"].cursor()
cursor.execute("SELECT COUNT(*) FROM Documents")
sql_count = cursor.fetchone()[0]
st.sidebar.metric("💾 SQL Documents", sql_count)

st.sidebar.markdown("---")
st.sidebar.info("Make sure Neo4j, Ollama, and SQL Server are running!")

# =============================================================================
# MAIN: QUESTION INPUT
# =============================================================================
st.header("❓ Ask a Question")

question = st.text_input(
    "Type your question here:",
    placeholder="e.g., Who founded Tesla? What companies is Elon Musk connected to?"
)

col1, col2 = st.columns([1, 5])
with col1:
    ask_button = st.button("🔍 Ask GraphRAG", type="primary", use_container_width=True)
with col2:
    st.markdown("")  # Spacer

# =============================================================================
# ANSWER LOGIC
# =============================================================================
if ask_button and question:
    with st.spinner("Thinking... Running GraphRAG pipeline..."):
        
        # STEP 1: Vector Search
        st.subheader("🔍 Step 1: Vector Search (ChromaDB)")
        vector_results = systems["collection"].query(
            query_texts=[question],
            n_results=3
        )
        chunks = vector_results['documents'][0]
        
        with st.expander("📄 See similar text chunks found"):
            for i, chunk in enumerate(chunks):
                st.write(f"**{i+1}.** {chunk}")
        
        # STEP 2: Graph Search
        st.subheader("🕸️ Step 2: Graph Search (Neo4j)")
        
        # Extract potential entities from question
        doc = systems["nlp"](question)
        question_entities = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG"]]
        
        # Also check common ones
        common = ["Elon Musk", "Tesla", "SpaceX", "Martin Eberhard", 
                  "Marc Tarpenning", "Maxwell Technologies"]
        found_entities = list(set([e for e in common if e.lower() in question.lower()] + question_entities))
        
        graph_data = []
        with systems["neo4j"].session() as session:
            for entity in found_entities:
                result = session.run("""
                    MATCH (e:Entity {name: $name})-[r]-(c)
                    RETURN e.name as source, type(r) as relation, c.name as target
                    LIMIT 5
                """, name=entity)
                for record in result:
                    graph_data.append({
                        "Source": record["source"],
                        "Relation": record["relation"],
                        "Target": record["target"]
                    })
        
        if graph_data:
            with st.expander("🔗 See graph connections found"):
                st.table(graph_data)
        else:
            st.info("No direct graph connections found for this question.")
        
        # STEP 3: LLM Answer
        st.subheader("🤖 Step 3: LLM Answer")
        
        prompt = f"""You are a helpful assistant. Use ONLY the provided context to answer the question.
If the context doesn't contain the answer, say "I don't have enough information."

--- TEXT CONTEXT ---
{chr(10).join(chunks)}

--- GRAPH CONNECTIONS ---
{json.dumps(graph_data, indent=2)}

--- QUESTION ---
{question}

--- ANSWER ---
"""
        
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.2", "prompt": prompt, "stream": False},
                timeout=60
            )
            answer = response.json()['response']
            
            # Display answer in a nice box
            st.success(answer)
            
        except Exception as e:
            st.error(f"⚠️ Ollama LLM not available: {e}")
            st.warning("Quick answer from vector search:")
            st.write(chunks[0] if chunks else "No information found.")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("Built with ❤️ using Python, Neo4j, ChromaDB, spaCy, Ollama, and Streamlit")