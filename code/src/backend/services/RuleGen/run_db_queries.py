from pymongo import MongoClient
import os
from services.base_mongo_service import BaseMongoService

# MongoDB Configuration
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = "DataProfiling"
COLLECTION_NAME = "Test_Rules"
TARGET_COLLECTION = "PDFName_ScheduleA_USAutoLoan_Data"

def setup_and_run_queries():
    """
    Set up the MongoDB client and use BaseMongoService to run queries fetched from the database.
    """
    client = MongoClient(MONGO_URI)
    base_mongo_service = BaseMongoService(client, COLLECTION_NAME, DB_NAME)

    try:
        # Fetch all queries from the database
        queries = base_mongo_service.get_all()

        for query_doc in queries:
            query = query_doc.get("query")
            if query:
                print(f"Running query: {query}")
                # Run the query using BaseMongoService
                results = base_mongo_service.run_mongo_cli_query(query, collection_name=TARGET_COLLECTION)
                print(f"Results: {len(results)}")
            else:
                print(f"No query found in document: {query_doc}")
    except Exception as e:
        print(f"Error while running queries: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    setup_and_run_queries()
