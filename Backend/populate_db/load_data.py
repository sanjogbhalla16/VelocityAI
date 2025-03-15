import json
import time
import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from split_f1_data import split_f1_data  # ✅ Import Q&A splitter
from create_collection import get_astra_collection  # ✅ Import AstraDB collection setup

# ✅ Load environment variables
load_dotenv()

# ✅ Get environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
input_data = os.getenv("SCRAPED_FILE")
model = os.getenv("VECTOR_MODEL")

# ✅ Initialize LangChain embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model=model) if model else OpenAIEmbeddings(openai_api_key=openai_api_key)

def get_input_data():
    print(f"📂 Loading data from: {input_data}")  # Debugging step

    if not os.path.exists(input_data):
        raise FileNotFoundError(f"❌ File not found: {input_data}")

    with open(input_data, "r") as f:
        return json.load(f)

async def embed(text_to_embed):
    """Converts text into vector embeddings using LangChain."""
    return await embeddings.aembed_query(text_to_embed)  # ✅ Corrected async embedding

async def main():
    """Processes scraped F1 data, extracts Q&A pairs, and stores them in AstraDB."""
    collection = get_astra_collection()  # ✅ Get AstraDB collection

    # ✅ Load scraped F1 data
    input_data_f1 = get_input_data()

    # ✅ Process scraped F1 data
    for webpage in input_data_f1:
        q_and_a_data = split_f1_data(webpage)  # ✅ Extract Q&A pairs

        for i, (question, answer) in enumerate(zip(q_and_a_data["questions"], q_and_a_data["answers"])):
            # Skip malformed data
            if question.strip() in ["", "?", " Cluster?"]:
                print("⚠️ Skipping malformed question.")
                continue

            # ✅ Generate embedding
            embedding = await embed(question)
            time.sleep(1)  # ✅ Avoid rate limits

            # ✅ Prepare document for AstraDB
            to_insert = {
                "document_id": webpage["url"],
                "question_id": i + 1,
                "question": question,
                "answer": answer,
                "$vector": embedding
            }

            # ✅ Insert into AstraDB
            collection.insert_one(to_insert)
            print(f"✅ Inserted: {question}")

if __name__ == "__main__":
    asyncio.run(main())  # ✅ Run async function
