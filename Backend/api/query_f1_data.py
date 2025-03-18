from openai import OpenAI
import os
from dotenv import load_dotenv
from populate_db.create_collection import get_astra_collection
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI client
client = OpenAI()

collection = get_astra_collection()  # ✅ Get AstraDB collection

def get_best_answer(query, k=3):
    """
    Retrieves the most relevant F1 answers from AstraDB using vector search.
    """
    # ✅ Generate embedding for the query
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query,
        encoding_format="float"
    )
    
    query_embedding = response["data"][0]["embedding"]
    
    relevant_docs = collection.vector_find(query_embedding, limit=k)
    
    # ✅ Extract answers and URLs
    answers = [doc["answer"] for doc in relevant_docs]
    urls = [doc["url"] for doc in relevant_docs]
    
    # ✅ Combine retrieved answers
    retrieved_info = "\n".join(answers)

    return retrieved_info, urls[0] if urls else "N/A"