from pymongo import MongoClient

def save_keywords_to_db(keywords):
    # Connect to the MongoDB server
    client = MongoClient('localhost', 27017)  # Adjust the host and port if necessary
    
    # Access the database
    db = client['markets']
    
    # Access the collection
    collection = db['keywords']
    
    # Keep track of inserted keywords count
    inserted_count = 0

    for keyword in keywords:
        # Check if the keyword already exists in the collection
        if collection.count_documents({'keyword': keyword}, limit=1) == 0:
            # Insert the keyword if it does not exist
            collection.insert_one({'keyword': keyword})
            inserted_count += 1
    
    # Print the result of the insertion
    print(f'{inserted_count} new keywords inserted.')
    
    # Close the connection
    client.close()

# Example usage
if __name__ == "__main__":
    keywords = ['arroz', 'café', 'huevos', 'aceite', 'pan']
    save_keywords_to_db(keywords)
