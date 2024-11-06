import streamlit as st
import requests
import json

# API URL for Flask backend
API_URL = "http://localhost:5000/llm_reply"

def call_llm_api(query, filenames):
    """Function to call the Flask API and get the response."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "query": query,
        "filenames": filenames
    }
    
    try:
        # Make the POST request to the Flask API
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            st.error("Error: " + response.text)
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

def main():
    st.title("Query to LLM")

    # User input for query and filenames
    query = st.text_input("Enter your query:")
    
    filenames_input = st.text_input("Enter filenames (comma separated, without extensions):")
    filenames = filenames_input.split(",") if filenames_input else []
    
    if st.button("Submit Query"):
        if query and filenames:
            # Call the Flask API
            result = call_llm_api(query, filenames)
            
            if result:
                # Display the response from the API
                st.subheader("Response from LLM:")
                st.write(result.get("message"))
                st.write(f"Query: {result.get('query')}")
                st.write(f"Filenames: {result.get('filename')}")
        else:
            st.error("Please enter both a query and filenames!")

if __name__ == "__main__":
    main()
