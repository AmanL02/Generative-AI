Here’s the formatted *Installation* section for your README file:

---

## Installation

To set up and run the application, follow these steps:

### 1. Clone the Repository
Clone the repository to your local machine:

bash
git clone https://github.com/AmanL02/Generative-AI.git
cd Gen AI


### 2. Install Poetry
If you haven't installed Poetry yet, follow the [Poetry installation guide](https://python-poetry.org/docs/#installation). Once Poetry is installed, you can use it to manage your dependencies.

### 3. Install Dependencies with Poetry
Use the following command to install all required dependencies:

bash
poetry install


### 4. Activate the Virtual Environment
Poetry automatically creates a virtual environment for you. You can activate it with:

bash
poetry shell


### 5. Start ChromaDB
Make sure you have *ChromaDB* running locally on port 8000. You can install it and run it using the [ChromaDB installation guide](https://www.chromadb.com/docs). This will be needed to store document embeddings and perform similarity searches.

### 6. Run the Flask Server
Once your environment is set up and ChromaDB is running, you can start the Flask application:

bash
python server.py


The server will be available at http://localhost:5000.

---

### 7. Run streamlit

This section will be part of your README file for easy reference on how to set up the project with Poetry and Flask.
