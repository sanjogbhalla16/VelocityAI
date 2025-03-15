import json
import time
import os
import asyncio
import uuid  # ✅ Import UUID for unique document IDs
from dotenv import load_dotenv
from openai import OpenAI
from split_f1_data import split_f1_data  # ✅ Import Q&A splitter
from create_collection import get_astra_collection  # ✅ Import AstraDB collection setup

# ✅ Load environment variables
load_dotenv()

# ✅ Get environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
input_data = os.getenv("SCRAPED_FILE")
model = os.getenv("VECTOR_MODEL")

# ✅ Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

def get_input_data():
    """Loads scraped F1 data from a JSON file."""
    print(f"📂 Loading data from: {input_data}")  # Debugging step

    if not os.path.exists(input_data):
        raise FileNotFoundError(f"❌ File not found: {input_data}")

    with open(input_data, "r") as f:
        return json.load(f)

async def embed(text_to_embed):
    """Generates embeddings using OpenAI's API."""
    response = await client.embeddings.create(
        model="text-embedding-ada-002",
        input=text_to_embed,
        encoding_format="float"
    )
    
    embedding = response.data[0].embedding  # ✅ Extract embedding vector
    
    # ✅ Debugging: Print embedding size
    print(f"🧠 Generated embedding of size {len(embedding)} for: {text_to_embed[:50]}...")

    return embedding


async def main():
    """Processes scraped F1 data, extracts Q&A pairs, and stores them in AstraDB."""
    collection = get_astra_collection()  # ✅ Get AstraDB collection

    # ✅ Load scraped F1 data
    input_data_f1 = get_input_data()

    # ✅ Process scraped F1 data
    for webpage in input_data_f1:
        q_and_a_data = split_f1_data(webpage)  # ✅ Extract Q&A pairs

        for i, (question, answer) in enumerate(zip(q_and_a_data["questions"], q_and_a_data["answers"])):
            # ✅ Skip malformed data
            if question.strip() in ["", "?", " Cluster?"]:
                print("⚠️ Skipping malformed question.")
                continue

            # ✅ Generate embedding using OpenAI SDK
            embedding = await embed(question)
            await asyncio.sleep(1)  # ✅ Use async sleep to avoid blocking

            # ✅ Prepare document for AstraDB
            to_insert = {
                "document_id": str(uuid.uuid4()),  # ✅ Unique document ID
                "source_url": webpage["url"],
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
