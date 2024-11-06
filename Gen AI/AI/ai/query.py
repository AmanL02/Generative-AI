import chromadb
from sentence_transformers import SentenceTransformer

def get_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # You can replace with other models
    embedding = model.encode(text)
    return embedding

def main():
    # Connect to Chroma server
    chroma = chromadb.HttpClient(host="localhost", port=8000)
    collection = chroma.get_or_create_collection("test")

    query = input('What would you like to know about the text? ')

    # Get embedding using sentence-transformers
    prompt_embedding = get_embedding(query)

    # Ensure query_embeddings is a list of embeddings (each embedding is a list)
    query_embeddings = [prompt_embedding]  # Wrap it in a list

    # Query Chroma database with the embedding
    result = collection.query(query_embeddings=query_embeddings, n_results=10)

    relevant_docs = result.get("documents", [])
    
    # Print the relevant documents
    if relevant_docs:
        for doc in relevant_docs:
            print(doc)
    else:
        print("No relevant documents found.")
    
    print("Prompt Embedding:", prompt_embedding)

# Run the main function
main()
