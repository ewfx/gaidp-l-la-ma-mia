import csv
import json
import requests
import os
import openai

# CONFIG
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = "llama-3.3-70b-versatile"  # or use gemma-7b-it
CSV_FILE_PATH = "audit_rules_groq.csv"
CONSTRAINT_COLUMN = "Rule"

# Function to call Groq LLM
def get_mongo_query_from_llm(constraint):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert in MongoDB. Write a Mongo query to find all the records that violate the contraints. Give me ONLY the query. Do not put newline characters in the query."},
            {"role": "user", "content": f"We have the following the constraint(<Column name>: <constraint>): {constraint}"}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    try:
        query = result["choices"][0]["message"]["content"].strip()
        return query
    except Exception as e:
        print(f"Error parsing response: {e}")
        return ""

def get_mongo_query_using_openai(constraint):
    openai.api_key = GROQ_API_KEY
    openai.base_url = "https://api.groq.com/openai/v1/"  # Important: override base_url for Groq

    try:
        response = openai.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in MongoDB. Write a Mongo query to find all the records that violate the contraints. Give me ONLY the query. Do not put newline characters in the query."},
                {"role": "user", "content": f"We have the following the constraint(<Column name>: <constraint>): {constraint}"}
            ],
            temperature=0.3
        )
        query = response.choices[0].message.content.strip()
        return query
    except Exception as e:
        print(f"OpenAI-Groq Error: {e}")
        return ""

# Read CSV and process constraints
def process_csv_and_generate_queries():
    queries = []
    with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            constraint = row.get(CONSTRAINT_COLUMN)
            if constraint:
                print(f"Processing constraint: {constraint}")
                # mongo_query = get_mongo_query_from_llm(constraint)
                mongo_query = get_mongo_query_using_openai(constraint)
                queries.append({"constraint": constraint, "mongo_query": mongo_query})
    return queries

# Save output as JSON
def save_queries_to_json(queries, output_file="mongo_queries_output.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(queries, f, indent=2)

if __name__ == "__main__":
    results = process_csv_and_generate_queries()
    save_queries_to_json(results)
    print(f"\nSaved {len(results)} queries to mongo_queries_output.json")
