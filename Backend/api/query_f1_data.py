from openai import OpenAI
import os
from dotenv import load_dotenv
import sys
# ✅ Get the absolute path of the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from populate_db.create_collection import get_astra_collection
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI client
client = OpenAI()

collection = get_astra_collection()  # ✅ Get AstraDB collection

query = "Who is the Fastest Driver?"
async def get_best_answer(query: str, k=3):
    """
    Retrieves the most relevant F1 answers from AstraDB using vector search.
    """
    # ✅ Generate embedding for the query
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query,
        encoding_format="float"
    )
    
    query_embedding = response.data[0].embedding
    
    cursor = collection.find(
        filter={},
        sort={"$vector": query_embedding},  # Vector-based search
        limit=k
    )
    
    relevant_docs = list(cursor)  # ✅ Correct way to extract documents


    # ✅ Extract answers and URLs safely
    answers = [doc["answer"] for doc in relevant_docs]
    urls = [doc.get("source_url", "N/A") for doc in relevant_docs]  

    # ✅ Combine retrieved answers
    retrieved_info = "\n".join(answers)
    
    print(retrieved_info, urls[0] if urls else "N/A")
    return retrieved_info, urls[0] if urls else "N/A"