from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Initialize models
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Store paragraphs and their embeddings in memory (no database)
stored_paragraphs = []
stored_embeddings = []

def parse_file(filename):
    with open(filename, encoding='utf-8-sig') as f:
        paragraphs = []
        buffer = []
        for line in f.readlines():
            line = line.strip()
            if line:
                buffer.append(line)
            elif len(buffer):
                paragraphs.append((' ').join(buffer))
                buffer = []
        if len(buffer):
            paragraphs.append((' ').join(buffer))
        return paragraphs

@app.route('/', methods=['GET'])
def api_health_checker():
    response_data = {
        "success": True,
        "message": "Python Flask backend is up and running!"
    }
    return jsonify(response_data), 200

@app.route('/llm_reply', methods=['POST'])
def get_resource():
    json_data = request.json
    query = json_data.get('query')

    SYSTEM_PROMPT = """You are a helpful reading assistant who answers questions 
        based on snippets of text provided in context. Answer only using the context provided, 
        being as concise as possible. If you're unsure, just say that you don't know.
        Context:
    """

    file_names = json_data.get('filenames')
    out_files = file_names[-1]
    file_final = f'D:/Gen AI/AI/output/{out_files}'
    
    # Parse the file and generate embeddings for the paragraphs
    paragraphs = parse_file(file_final)
    
    global stored_paragraphs, stored_embeddings
    for index, chunk in enumerate(paragraphs):
        embedding = embedding_model.encode(chunk)
        stored_paragraphs.append(chunk)
        stored_embeddings.append(embedding)
    
    # Embed the query
    query_embedding = embedding_model.encode(query)
    
    # Compute cosine similarity between the query and all stored embeddings
    similarities = cosine_similarity([query_embedding], stored_embeddings)[0]

    # Get the index of the most similar paragraph (top 1)
    top_index = similarities.argmax()  # This gives the index of the highest similarity

    # Get the most relevant document
    relevant_doc = stored_paragraphs[top_index]
    print("hello", relevant_doc)

    # # Prepare context from the most relevant document
    # context = SYSTEM_PROMPT + relevant_doc

    # # Generate response based on context and query
    # response = chat_pipeline(context + query, max_length=100, num_return_sequences=1)[0]['generated_text']

    response_data = {
        "success": True,
        "query": query,
        "filename": file_names,
        "message": relevant_doc  # Only the generated part
    }

    return jsonify(response_data), 200

def main():
    app.run(debug=True)

main()
