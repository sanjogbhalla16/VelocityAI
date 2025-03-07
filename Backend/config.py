# Python-dotenv reads key-value pairs from a .env file and can set them as environment variables
import os
from dotenv import load_dotenv

load_dotenv()

#Get an environment variable, return None if it doesn't exist.
#The optional second argument can specify an alternate default.
#key, default and the result are str
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

