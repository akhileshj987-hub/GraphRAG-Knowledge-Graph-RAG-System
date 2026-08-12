import os

def load_documents(folder_path="documents"):
    """
    Reads all .txt files from the documents folder
    and returns them as a list of dictionaries.
    """
    documents = []
    
    # Get the full path to the documents folder
    full_path = os.path.join(os.path.dirname(__file__), folder_path)
    
    # Loop through all files in the folder
    for filename in os.listdir(full_path):
        if filename.endswith(".txt"):  # Only read .txt files
            file_path = os.path.join(full_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            documents.append({
                "id": filename,
                "content": content,
                "path": file_path
            })
            
            print(f"✅ Loaded: {filename} ({len(content)} characters)")
    
    return documents

# Test the function
if __name__ == "__main__":
    docs = load_documents()
    print(f"\n📁 Total documents loaded: {len(docs)}")
    
    # Show first 200 characters of each document
    for doc in docs:
        print(f"\n--- {doc['id']} ---")
        print(doc['content'][:200] + "...")