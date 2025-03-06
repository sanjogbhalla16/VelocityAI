import chromadb

chromadb_client = chromadb.Client() #the client is used to connect to the database

#create a collection
collection = chromadb_client.create_collection(name="my_villan_collection")