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

> 🔥 *Same architecture Microsoft, Google & Bloomberg use for enterprise search.*

---

## ✨ Key Features

| 🚀 Feature | 💡 What It Does |
|:----------:|:----------------|
| 🕸️ **Knowledge Graph** | Stores people, companies & relationships in Neo4j |
| 🔍 **Vector Search** | Finds similar text using ChromaDB embeddings |
| 🧠 **Multi-hop Reasoning** | Connects facts across documents (e.g., Person → Company → CEO) |
| 🤖 **Local LLM** | Uses Ollama (Llama 3.2) — no internet needed |
| 🛡️ **Zero Hallucination** | Only answers from YOUR documents |
| 💾 **SQL Tracking** | Microsoft SQL Server logs all metadata |
| 🌐 **Web UI** | Beautiful Streamlit interface |
| 🔒 **Privacy First** | Data never leaves your computer |

---

## 🏗️ System Architecture
## 🏗️ System Architecture

```mermaid
graph TD
    A[📄 Documents<br/>(.txt files)] --> B[🐍 Python Pipeline]
    B --> C[🔍 spaCy NER]
    B --> D[📊 ChromaDB<br/>Vector DB]
    C --> E[🕸️ Neo4j<br/>Knowledge Graph]
    E --> F[🤖 Ollama LLM]
    D --> F
    F --> G[🌐 Streamlit<br/>Web UI]
    B --> H[💾 SQL Server<br/>Metadata]
    
    style A fill:#e1f5fe
    style E fill:#fff3e0
    style F fill:#e8f5e9
    style G fill:#fce4ec
    style H fill:#f3e5f5
