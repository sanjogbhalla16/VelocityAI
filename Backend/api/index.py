from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from query_f1_data import get_best_answer
from openai import OpenAI
import os
from dotenv import load_dotenv
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from populate_db.chat_db import insert_chat,get_recent_chats
# we need to make the changes here

#A "middleware" is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.

load_dotenv()

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI client
client = OpenAI()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query:str
    

# we are posting our query here 
@app.post("/api/chat")
async def fill_and_send_prompt(query:Query):
    """Handles F1 chatbot queries with RAG-based responses."""
    
    # ✅ Step 1: Retrieve relevant F1 knowledge from AstraDB
    retrieved_answer,source_url = await get_best_answer(query.query)
    
    past_chats = get_recent_chats(limit=5)
    
    # history_text = ""
    # for user, bot in past_chats:
    # history_text += f"User: {user}\nBot: {bot}\n\n"

    
    # ✅ Format chat history into context
    history_text = "\n".join([f"User: {user}\nBot: {bot}" for user, bot in past_chats])
    
    prompt = f"""
    You are an expert in the field of F1 Racing and also has all the features of a chatbot.
    
    **Past Conversations:**
    {history_text}

    **Current User Question:** {query.query}

    **Retrieved F1 Knowledge:** 
    {retrieved_answer}
    
    **Instructions:**
    - Use both the chat history and retrieved F1 knowledge to give the best answer.
    - If the answer is in the F1 knowledge, prioritize that.
    - If the user refers to past chats, try to maintain context.
    - If no relevant information is available, say: "I don't have that information right now, but I can try to help!"

    **Final Answer:**    
    """
    
    # ✅ Step 2: Generate a response based on the retrieved knowledge
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are an expert in the field of F1 Racing and also has all the features of a chatbot."},
            {"role":"user","content":f"{retrieved_answer}\n\nUser question: {query.query}"},
        ],
        max_tokens=150
    )
    
    bot_response = response.choices[0].message.content.strip()
    
     # ✅ Step 4: Store the conversation in SQLite
    insert_chat(query.query, bot_response)
    print(bot_response)
    return {"text": bot_response, "source": source_url}
    



