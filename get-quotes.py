import requests
import json
import pymongo

def get_db():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017"
 
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = pymongo.MongoClient(CONNECTION_STRING)
    if client:
        print("DB Connected")
  
    # Create the database for our example (we will use the same database throughout the tutorial
    return client.webtools2.quotes

if __name__ == "__main__":
    db = get_db()
    
    count = 0
    miss_count = 0

    while miss_count < 10 and count < 200:
        print(f"Total {db.estimated_document_count()}:\n\tNew {count}\tMiss: {miss_count}")
        quote = requests.get("https://api.quotable.io/random")
        if quote.json()["_id"]:
            check_id = quote.json()["_id"]
            try:
                db.insert_one(quote.json())
                count += 1
            except(pymongo.errors.DuplicateKeyError):
                miss_count += 1
        else:
            print(f"No id found for {quote.json()}")

