from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

# ✅ Load environment variables
load_dotenv()

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def generate_question(text_chunk):
    """Generates a question based on a text chunk using OpenAI."""
    if not openai_api_key:
        raise ValueError("❌ OPENAI_API_KEY is missing. Check your .env file!")

    # ✅ Debugging: Check input chunk
    print(f"🔹 Generating question for: {text_chunk[:100]}...")  # Print first 100 chars
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that generates quiz questions from text."},
            {"role": "user", "content": f"Generate a question based on the following text:\n{text_chunk}\n\nQuestion:"}
        ],
        max_tokens=50
    )
    
    # ✅ Debugging: Print response
    print(f"📝 OpenAI Response: {response}")

    return response.choices[0].message.content.strip() if response.choices else None

def extract_answer(question,text_chunk):
    """Extracts a relevant answer from the text chunk for a given question."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that extracts concise answers from F1 race reports."},
            {"role":"user","content":f"Extract a relevant answer from the following text:\n{text_chunk}\n\nQuestion: {question}\nAnswer:"}
        ],
        max_tokens=50
    )
    
    raw_text = response.choices[0].message.content.strip() 
    
    # ✅ Remove any leading questions from the answer using regex
    answer = re.sub(r"^.*\?", "", raw_text).strip() if response.choices else None
    
    print(answer)
    
    return answer

def split_f1_data(input_text):
    """
    Processes F1-related scraped text into structured questions and answers.
    
    Args:
        input_text (dict): Dictionary with "title" and "content" keys.
    
    Returns:
        dict: Structured Q&A format.
    """
    text = input_text["content"]

    # Split content into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_text(input_text["content"])

    questions = []
    answers = []

    for chunk in text_chunks:
        question = generate_question(chunk)  # ✅ Generate a question dynamically
        if question:
            answer = extract_answer(question,chunk)  # ✅ Extract an answer dynamically
            if answer and not answer.startswith(question):
                questions.append(question)
                answers.append(answer)

    return {
        "title": input_text.get("title", "Untitled F1 Report"),
        "questions": questions,
        "answers": answers
    }
