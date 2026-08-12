# test_setup.py
import neo4j
import chromadb
import spacy

print("✅ Neo4j version:", neo4j.__version__)
print("✅ ChromaDB imported successfully")
print("✅ spaCy imported successfully")

# Test spaCy NER
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
for ent in doc.ents:
    print(f"Entity: {ent.text}, Type: {ent.label_}")