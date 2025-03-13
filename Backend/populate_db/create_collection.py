import os 
import sys
from dotenv import load_dotenv
from astrapy.db import AstraDB

# Load environment variables
load_dotenv()


# Fetch AstraDB credentials
token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
namespace = os.getenv("ASTRA_DB_NAMESPACE")
collection_name = os.getenv("ASTRA_DB_COLLECTION")
dimension = os.getenv("VECTOR_DIMENSION")


#check if dimension is set
if dimension is None:
    print("Please set the VECTOR_DIMENSION environment variable to the desired dimension")
    sys.exit()
elif not dimension.isdigit():
    print("VECTOR_DIMENSION must be an integer")
    sys.exit()

dimension = int(dimension)  # Convert to integer ✅

# Create AstraDB client 
if not namespace:
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
elif namespace:
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint, namespace=namespace)


# checks if the collection is there previously 
existing_collections = astra_db.get_collections().get('status',{}).get('collections',[])


if collection_name in existing_collections:
    print(f"✅ Collection '{collection_name}' already exists. No new collection created.")
else:
    # ✅ Create collection
    astra_db.create_collection(collection_name=collection_name, dimension=dimension)
    print(f"🎉 Collection '{collection_name}' created successfully!")