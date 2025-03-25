import csv
import json
import requests
import os
import openai
from pymongo import MongoClient
from services.base_mongo_service import BaseMongoService

# CONFIG
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = "llama-3.3-70b-versatile"  # or use gemma-7b-it
CSV_FILE_PATH = "audit_rules_groq.csv"
CONSTRAINT_COLUMN = "Rule"

# MongoDB Configuration
MONGO_URI = "mongodb+srv://agastya:Z3jVqmynjUQk5E7d@cluster0.wbyds.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "DataProfiling"
COLLECTION_NAME = "Test_Rules"

def get_mongo_query_using_openai(field_name, constraint):
    openai.api_key = GROQ_API_KEY
    openai.base_url = "https://api.groq.com/openai/v1/"  # Important: override base_url for Groq

    try:
        response = openai.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in MongoDB. Write a Mongo query to find all the records that VIOLATE the contraints. Make sure to check the data type wherever applicable and remember ne cannot be used to check type, not has to be used. Give me ONLY the query. Do not put newline characters in the query."},
                {"role": "user", "content": f"We have the following fieldName and constraint(<Column name>: <constraint>): {field_name}: {constraint}"}
            ],
            temperature=0.3
        )
        query = response.choices[0].message.content.strip()
        return query
    except Exception as e:
        print(f"OpenAI-Groq Error: {e}")
        return ""
    
def fix_mongo_query(query):
    openai.api_key = GROQ_API_KEY
    openai.base_url = "https://api.groq.com/openai/v1/"  # Important: override base_url for Groq

    try:
        response = openai.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in MongoDB. Fix the Mongo query for syntax errors given by the user. Especially focus on type checks and remember ne cannot be used to check type, not has to be used. Give me ONLY the corrected query or the original query, if there are no errors. Do not put newline characters in the query."},
                {"role": "user", "content": f"Check and fix this mongo query for syntax errors and return me only the query and NO other text: {query}"}
            ],
            temperature=0
        )
        query = response.choices[0].message.content.strip()
        return query
    except Exception as e:
        print(f"OpenAI-Groq Error: {e}")
        return ""
    
def format_mongo_query(query):
    openai.api_key = GROQ_API_KEY
    openai.base_url = "https://api.groq.com/openai/v1/"  # Important: override base_url for Groq

    try:
        response = openai.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in MongoDB and Python. Format the Mongo query so that the string can be converted to a dictionary in python, especially remember to enclose $<> operations in double quotes. Give me ONLY the formatted query. Do not put newline characters in the query or any extra text."},
                {"role": "user", "content": f"Check and format this mongo query so it can be converted into a python dictionary. give me only the dictionary and NO other text: {query}"}
            ],
            temperature=0
        )
        query = response.choices[0].message.content.strip()
        return query
    except Exception as e:
        print(f"OpenAI-Groq Error: {e}")
        return ""

# Updated function to fetch constraints from the database
def process_csv_and_generate_queries():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    base_mongo_service = BaseMongoService(client, COLLECTION_NAME, DB_NAME)

    try:
        for document in base_mongo_service.get_all():
            field_name = document.get("fieldName")
            rule = document.get("rule")
            mongo_query = get_mongo_query_using_openai(field_name, rule)
            print(mongo_query)
            fixed_mongo_query = fix_mongo_query(mongo_query)
            print(fixed_mongo_query)
            formatted_mongo_query = format_mongo_query(fixed_mongo_query)
            print(formatted_mongo_query)

            # Use the update method from BaseMongoService to update the query field
            base_mongo_service.update(
                document_id=str(document["_id"]),
                updated_data={"query": formatted_mongo_query}
            )
    finally:
        client.close()

if __name__ == "__main__":
    results = process_csv_and_generate_queries()
    # save_queries_to_json(results)
    print(f"\nSaved queries to DB!!!")
