import json
import time
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from astrapy.db import AstraDB
from split_f1_data import split_f1_data  # ✅ Import Q&A splitter

# Load environment variables
load_dotenv()

# here we get openAI key from env