&lt;p align="center"&gt;
  &lt;img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge&logo=chromadb&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" /&gt;
&lt;/p&gt;

&lt;h1 align="center"&gt;🕸️ GraphRAG System&lt;/h1&gt;
&lt;h3 align="center"&gt;Knowledge Graph + Vector Search + Local LLM for Private Document QA&lt;/h3&gt;

&lt;p align="center"&gt;
  &lt;b&gt;Multi-hop reasoning • Zero hallucination • 100% offline • Enterprise-ready&lt;/b&gt;
&lt;/p&gt;

&lt;p align="center"&gt;
  &lt;img src="https://img.shields.io/badge/Status-Working-brightgreen?style=flat-square" /&gt;
  &lt;img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" /&gt;
  &lt;img src="https://img.shields.io/badge/Last%20Updated-August%202026-blue?style=flat-square" /&gt;
&lt;/p&gt;

---

## 🎯 About The Project

&lt;p align="center"&gt;
  &lt;img src="https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge" /&gt;
  &lt;img src="https://img.shields.io/badge/Privacy-100%25_Offline-blue?style=for-the-badge" /&gt;
  &lt;img src="https://img.shields.io/badge/AI-GraphRAG-purple?style=for-the-badge" /&gt;
&lt;/p&gt;

**GraphRAG** is an intelligent, **privacy-first** document question-answering system that goes far beyond simple chatbots. Instead of calling an API like ChatGPT, it **reads your documents**, **builds a knowledge graph** of entities and relationships, and **answers complex multi-hop questions** by connecting facts across multiple files.

&gt; 🔥 *Same architecture Microsoft, Google & Bloomberg use for enterprise search.*

### 🔥 What Makes It Special?

| Feature | What It Means |
|:-------:|:--------------|
| 🕸️ **Knowledge Graph** | Stores people, companies & connections in Neo4j — not just text |
| 🔍 **Vector Search** | Finds meaning, not just keywords — powered by ChromaDB |
| 🧠 **Multi-hop Reasoning** | Answers questions like *"Who is the CEO of the company that acquired X?"* |
| 🤖 **Local LLM** | Uses Ollama (Llama 3.2) — **zero internet required** |
| 🛡️ **Zero Hallucination** | Only answers from **YOUR** documents — never makes up facts |
| 💾 **SQL Tracking** | Microsoft SQL Server logs every document processed |
| 🌐 **Web UI** | Beautiful Streamlit interface — just type and ask |
| 🔒 **Privacy First** | Data never leaves your computer |

---

## 📊 Live Results

```
┌─────────────────────────────────────────────┐
│  Documents Processed:        2 files        │
│  Neo4j Entities:             21 nodes       │
│  Neo4j Relationships:        11 edges       │
│  Vector Chunks:              9 chunks       │
│  SQL Server Records:         2 tracked      │
│  Web Interface:              Live           │
└─────────────────────────────────────────────┘
```

---

## 🎬 How It Works

**1️⃣ Ingest** → Drop `.txt` files into the `documents/` folder  
**2️⃣ Extract** → spaCy finds people, organizations, dates & locations  
**3️⃣ Graph** → Neo4j connects entities into a relationship network  
**4️⃣ Embed** → ChromaDB converts text into searchable vectors  
**5️⃣ Ask** → Type any question in the Streamlit web app  
**6️⃣ Answer** → Vector search + Graph traversal + LLM = Perfect answer  

---

## 🏢 Built For Real-World Use

&gt; 💼 **Enterprise Knowledge Management** — Search 1000s of internal PDFs  
&gt; ⚖️ **Legal Research** — Trace case connections across court documents  
&gt; 🏥 **Healthcare** — Connect patient records & research papers securely  
&gt; 📚 **Academic Research** — Map citations & findings across publications  

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Documents] --&gt; B[Python Pipeline]
    B --&gt; C[spaCy NER]
    B --&gt; D[ChromaDB Vector DB]
    C --&gt; E[Neo4j Knowledge Graph]
    E --&gt; F[Ollama LLM]
    D --&gt; F
    F --&gt; G[Streamlit Web UI]
    B --&gt; H[SQL Server Metadata]
    
    style A fill:#e1f5fe
    style E fill:#fff3e0
    style F fill:#e8f5e9
    style G fill:#fce4ec
    style H fill:#f3e5f5
```

---

## 🛠️ Tech Stack

&lt;p align="center"&gt;
  &lt;img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Neo4j-008CC1?style=flat&logo=neo4j&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=flat&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/spaCy-09A3D5?style=flat&logo=spacy&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Ollama-000000?style=flat&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white" /&gt;
  &lt;img src="https://img.shields.io/badge/VS%20Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white" /&gt;
&lt;/p&gt;

---

## 📊 Results

| Metric | Value |
|:------:|:-----:|
| 🕸️ Neo4j Entities | **21** |
| 🔗 Neo4j Relationships | **11** |
| 📄 Vector Chunks | **9** |
| 💾 SQL Documents Tracked | **2** |
| 📁 Documents Processed | `sample.txt`, `reliance.txt` |

---

## 🧪 Live Demo Questions

| Question | Answer |
|:---------|:-------|
| Who founded Tesla? | Martin Eberhard and Marc Tarpenning |
| Who founded Reliance? | Dhirubhai Ambani in 1966 |
| What companies is Elon Musk connected to? | Tesla, SpaceX |
| When was Reliance Jio launched? | 2016 |

---

## 🚀 Quick Start

### 1️⃣ Clone the repo
```bash
git clone https://github.com/akhileshj987-hub/GraphRAG-Knowledge-Graph-RAG-System.git
cd GraphRAG-Knowledge-Graph-RAG-System
```

### 2️⃣ Setup environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3️⃣ Start services
- **Neo4j Desktop** → Start `GraphRAG-DB`
- **Ollama** → Run `ollama serve` in a separate terminal
- **SQL Server** → Ensure `GraphRAG_DB` database exists

### 4️⃣ Run the pipeline
```bash
python main.py
```

### 5️⃣ Launch Web UI
```bash
streamlit run app.py
```
Then open 👉 `http://localhost:8501`

---

## 📂 Project Structure

```
GraphRAG-Knowledge-Graph-RAG-System/
├── 📁 documents/              # Your knowledge source files
│   ├── sample.txt
│   └── reliance.txt
├── 📁 chroma_db/              # Vector database storage
├── 🐍 app.py                  # Streamlit web interface
├── 🐍 main.py                 # Complete integration pipeline
├── 🐍 graph_rag.py            # Core GraphRAG engine
├── 🐍 entity_extraction.py    # spaCy NER → Neo4j
├── 🐍 build_relationships.py  # Relationship extraction
├── 🐍 vector_store.py         # ChromaDB vector storage
├── 🐍 sql_connection.py       # SQL Server metadata
├── 🐍 neo4j_connection.py     # Neo4j connection
├── 🐍 ingest_documents.py     # Document loader
└── 🐍 test_setup.py           # Installation verification
```

---

## 🖼️ Screenshots

&gt; *Add your screenshots here!*
&gt;
&gt; **Suggested screenshots to upload:**
&gt; 1. Neo4j Browser graph visualization
&gt; 2. Streamlit web app interface
&gt; 3. Terminal output showing successful pipeline run

---

## 🔮 Future Enhancements

- [ ] 📄 PDF & DOCX support (PyPDF2)
- [ ] 🌐 Deploy to Streamlit Cloud / AWS
- [ ] 🤖 OpenAI API integration option
- [ ] 📊 Interactive graph visualization in Streamlit
- [ ] 🔗 Multi-document comparison queries

---

## 🙋 Why Not Just Use ChatGPT API?

| Feature | ChatGPT API | This GraphRAG |
|:-------:|:-----------:|:-------------:|
| 🔒 Private documents | ❌ Risky | ✅ 100% offline |
| 🏢 Company internal data | ❌ No access | ✅ Perfect |
| 🧠 Multi-hop reasoning | ❌ Weak | ✅ Graph traversal |
| 💰 Cost | 💸 Per call | ✅ Free |
| 📍 Source citation | ❌ None | ✅ Exact document |

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

&lt;p align="center"&gt;
  &lt;b&gt;Built with ❤️ using Python, Neo4j, ChromaDB, spaCy, Ollama & Streamlit&lt;/b&gt;
&lt;/p&gt;
