import json
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from split_f1_data import split_f1_data  # ✅ Import Q&A splitter
from astra_db import get_astra_collection  # ✅ Import AstraDB collection setup

# Load environment variables
load_dotenv()

# Get environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
input_data = os.getenv("SCRAPED_FILE")
model = os.getenv("VECTOR_MODEL")

# ✅ Initialize LangChain embeddings
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model=model) if model else OpenAIEmbeddings(openai_api_key=openai_api_key)

async def get_input_data():
    """Loads scraped F1 data from a JSON file asynchronously."""
    async with asyncio.to_thread(open, input_data, 'r') as f:
        return json.load(f)  # ✅ Returns full scraped data

async def embed(text_to_embed):
    """Converts text into vector embeddings using LangChain asynchronously."""
    return await asyncio.to_thread(embeddings.embed_query, text_to_embed)

async def process_f1_data():
    """Processes scraped F1 data, extracts Q&A pairs, and stores them in AstraDB asynchronously."""
    collection = await asyncio.to_thread(get_astra_collection)  # ✅ Get AstraDB collection

    input_data_f1 = await get_input_data()  # ✅ Load scraped F1 data

    tasks = []  # List to store async tasks

    for webpage in input_data_f1:
        q_and_a_data = split_f1_data(webpage)  # Extract Q&A pairs

        for i, (question, answer) in enumerate(zip(q_and_a_data["questions"], q_and_a_data["answers"])):
            if question.strip() in ["", "?", " Cluster?"]:  # Skip malformed data
                print("⚠️ Skipping malformed question.")
                continue
            
            tasks.append(insert_into_db(collection, webpage["url"], i + 1, question, answer))  

            if len(tasks) >= 5:  # ✅ Batch insert every 5 questions to improve efficiency
                await asyncio.gather(*tasks)
                tasks.clear()

    if tasks:  # ✅ Insert any remaining tasks
        await asyncio.gather(*tasks)

async def insert_into_db(collection, document_id, question_id, question, answer):
    """Embeds the question, prepares the document, and inserts it into AstraDB asynchronously."""
    embedding = await embed(question)  # ✅ Generate embedding
    await asyncio.sleep(1)  # ✅ Avoid rate limits

    to_insert = {
        "document_id": document_id,
        "question_id": question_id,
        "question": question,
        "answer": answer,
        "$vector": embedding
    }

    await asyncio.to_thread(collection.insert_one, to_insert)  # ✅ Insert into AstraDB
    print(f"✅ Inserted: {question}")

if __name__ == "__main__":
    asyncio.run(process_f1_data())
