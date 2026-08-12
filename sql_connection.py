import pyodbc

# ⚠️ UPDATE THIS with your actual SQL Server name!
# Common examples:
#   "DESKTOP-ABC123\\SQLEXPRESS"
#   "localhost"
#   "localhost\\SQLEXPRESS"
#   "127.0.0.1"
SERVER = "UCHIHA\\SQLEXPRESS"  # <-- CHANGE THIS!
DATABASE = "GraphRAG_DB"

def connect_sql():
    """Connect to Microsoft SQL Server"""
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'Trusted_Connection=yes;'  # Uses Windows login
    )
    return conn

def store_document_metadata(doc_id, title, source_path, entity_count, relationship_count):
    """Save document info to SQL Server"""
    conn = connect_sql()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO Documents (doc_id, title, source_path, entity_count, relationship_count)
        VALUES (?, ?, ?, ?, ?)
    """, doc_id, title, source_path, entity_count, relationship_count)
    
    conn.commit()
    conn.close()
    print(f"✅ Saved to SQL Server: {doc_id}")

def get_all_documents():
    """Retrieve all tracked documents"""
    conn = connect_sql()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Documents")
    rows = cursor.fetchall()
    
    print("\n📊 Documents in SQL Server:")
    print("-" * 80)
    for row in rows:
        print(f"   📄 {row.doc_id} | Entities: {row.entity_count} | Rel: {row.relationship_count} | Date: {row.processed_date}")
    
    conn.close()
    return rows

# Test
if __name__ == "__main__":
    print("🔗 Connecting to SQL Server...")
    
    # Store sample data
    store_document_metadata(
        doc_id="sample.txt",
        title="Tesla & SpaceX History",
        source_path="C:\\...\\documents\\sample.txt",
        entity_count=10,
        relationship_count=4
    )
    
    # Retrieve all
    get_all_documents()