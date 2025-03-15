from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(openai_api_key=openai_api_key)

def generate_question(text):
    """Uses OpenAI to generate a relevant question based on the given text."""
    prompt = f"Generate a question based on the following information:\n{text}\n\nQuestion:"
    response = client.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def split_f1_data(input_text):
    """
    Processes F1-related scraped text into structured questions and answers.
    
    Args:
        input_text (dict): Dictionary with "title" and "content" keys.
    
    Returns:
        dict: Structured Q&A format.
    """
    output_dict = {"title": input_text["title"]}

    # Split content into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_text(input_text["content"])

    questions = []
    answers = []

    for chunk in text_chunks:
        question = generate_question(chunk)  # ✅ Generate a question dynamically
        if question:
            questions.append(question)
            answers.append(chunk)

    output_dict["questions"] = questions
    output_dict["answers"] = answers

    return output_dict
