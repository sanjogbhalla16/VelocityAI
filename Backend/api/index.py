from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from query_f1_data import get_best_answer
from openai import OpenAI
import os
from dotenv import load_dotenv

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
    retrieved_answer = get_best_answer(query.query)
    
    # ✅ Step 2: Generate a response based on the retrieved knowledge
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are an expert in the field of F1 Racing and also has all the features of a chatbot."},
            {"role":"user","content":f"{retrieved_answer}\n\nUser question: {query.prompt}"},
        ],
        max_tokens=150
    )
    
    bot_response = response.choices[0].message.content.strip()
    return json.dump({"text":bot_response}) 
    
    


