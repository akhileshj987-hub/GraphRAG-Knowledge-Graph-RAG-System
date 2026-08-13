<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13.7-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge&logo=chromadb&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" />
</p>

<h1 align="center">🕸️ GraphRAG System</h1>
<h3 align="center">Knowledge Graph + Vector Search + Local LLM for Private Document QA</h3>

<p align="center">
  <b>Multi-hop reasoning • Zero hallucination • 100% offline • Enterprise-ready</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Working-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/Last%20Updated-August%202026-blue?style=flat-square" />
</p>

---

## 🎯 What is GraphRAG?

GraphRAG goes beyond simple chatbots. It **reads your documents**, **builds a knowledge graph** of entities & relationships, and **answers complex questions** by connecting facts across multiple files.

---
## 🎯 About The Project

<p align="center">
  <img src="https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Privacy-100%25_Offline-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-GraphRAG-purple?style=for-the-badge" />
</p>

**GraphRAG** is an intelligent, **privacy-first** document question-answering system that goes far beyond simple chatbots. Instead of calling an API like ChatGPT, it **reads your documents**, **builds a knowledge graph** of entities and relationships, and **answers complex multi-hop questions** by connecting facts across multiple files.

> 🔥 *Same architecture Microsoft, Google & Bloomberg use for enterprise search.*

---

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


## 📊 Results

| Metric | Value |
|:------:|:-----:|
| 🕸️ Neo4j Entities | **21** |
| 🔗 Neo4j Relationships | **11** |
| 📄 Vector Chunks | **9** |
| 💾 SQL Documents Tracked | **2** |
| 📁 Documents Processed | `sample.txt`, `reliance.txt` |

## 🏢 Built For Real-World Use

> 💼 **Enterprise Knowledge Management** — Search 1000s of internal PDFs  
> ⚖️ **Legal Research** — Trace case connections across court documents  
> 🏥 **Healthcare** — Connect patient records & research papers securely  
> 📚 **Academic Research** — Map citations & findings across publications  

---
## 🏗️ System Architecture

```mermaid
graph TD
    A[Documents] --> B[Python Pipeline]
    B --> C[spaCy NER]
    B --> D[ChromaDB Vector DB]
    C --> E[Neo4j Knowledge Graph]
    E --> F[Ollama LLM]
    D --> F
    F --> G[Streamlit Web UI]
    B --> H[SQL Server Metadata]
    
    style A fill:#e1f5fe
    style E fill:#fff3e0
    style F fill:#e8f5e9
    style G fill:#fce4ec
    style H fill:#f3e5f5
