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

# ✅ Ensure VECTOR_DIMENSION is set and valid
if not dimension or not dimension.isdigit():
    print("❌ ERROR: Please set a valid VECTOR_DIMENSION environment variable.")
    sys.exit()

dimension = int(dimension)  # Convert to integer ✅

# ✅ Initialize AstraDB client
astra_client = DataAPIClient(token=token)

# ✅ Get database reference
database = astra_client.get_database(api_endpoint)

# ✅ Try getting collection; create it if it doesn't exist
try:
    collection = database.get_collection(collection_name)
    print(f"✅ Collection '{collection_name}' already exists.")
except Exception as e:
    print(f"🚀 Collection '{collection_name}' not found. Creating a new one...")
    try:
        database.create_collection(collection_name, dimension)  # ✅ Correct method
        collection = database.get_collection(collection_name)  # ✅ Get the new collection
        print(f"🎉 Collection '{collection_name}' created successfully!")
    except Exception as e:
        print(f"❌ ERROR: Failed to create collection. Details: {e}")
        sys.exit()

# ✅ Function to return Astra collection
def get_astra_collection():
    print(f"✅ Returning collection: '{collection_name}'")
    return collection  # ✅ Use the already created/retrieved collection
