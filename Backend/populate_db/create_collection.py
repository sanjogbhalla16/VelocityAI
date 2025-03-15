import os
import sys
from dotenv import load_dotenv
from astrapy import DataAPIClient  # ✅ Correct import

# Load environment variables
load_dotenv()

# Fetch AstraDB credentials
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
namespace = os.getenv("ASTRA_DB_NAMESPACE")
collection_name = os.getenv("ASTRA_DB_COLLECTION")
dimension = os.getenv("VECTOR_DIMENSION")

# ✅ Ensure dimension is set and valid
if dimension is None:
    print("❌ ERROR: Please set the VECTOR_DIMENSION environment variable.")
    sys.exit()
elif not dimension.isdigit():
    print("❌ ERROR: VECTOR_DIMENSION must be an integer.")
    sys.exit()

dimension = int(dimension)  # Convert to integer ✅

# ✅ Initialize AstraDB client
astra_client = DataAPIClient(token=token)

# ✅ Get database reference
database = astra_client.get_database(api_endpoint)

# ✅ Get collection reference
try:
    collection = database.get_collection(collection_name)
    print(f"✅ Collection '{collection_name}' already exists.")
except Exception:
    print(f"🚀 Creating new collection '{collection_name}'...")
    database.create_collection(collection_name, dimension)  # ✅ Correct method
    print(f"🎉 Collection '{collection_name}' created successfully!")

# ✅ Function to return Astra collection
def get_astra_collection():
    print(f"✅ Collection '{collection_name}' returned.")
    return database.get_collection(collection_name)
