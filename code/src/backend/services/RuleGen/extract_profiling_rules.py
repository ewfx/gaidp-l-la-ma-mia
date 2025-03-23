# audit_rule_extractor_groq.py

"""
LLM-based Audit Rule Extractor for PDF Documents using Groq.com API (e.g., Mixtral or LLaMA3)
Requires a free Groq API key
"""

import os
import pdfplumber
import csv
import requests
from pymongo import MongoClient
from services.base_mongo_service import BaseMongoService  # Import BaseMongoService

# ========== 1. Load PDF and Extract Page-wise Text ==========
def extract_text_by_page(pdf_path):
    page_text = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                page_text[i] = text
    return page_text


# ========== 2. Extract Rules Using Groq LLM API ==========
def extract_rules_llm_groq(page_text, page_number, api_key, model="llama-3.3-70b-versatile"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"Extract data profiling rules from the following text for all variables / fields, make sure to only have 'variable : comma-separated rules' and no other extra text. Further where there are fixed values possible, mention that in the description :\n\n{page_text}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in understanding audit rules. You can read through a bunch of text and figure out the variables / fields in the data and the meaning of each field. You can translate the long descriptions into simple data profiling rules."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        output_text = result['choices'][0]['message']['content']
        rules = [line.strip('-• ') for line in output_text.split('\n') if len(line.strip()) > 10]
        return [(rule, page_number) for rule in rules]
    else:
        print(f"Error from Groq API (Page {page_number}):", response.text)
        return []


# ========== 3. Save Rules to List of Dictionaries ==========
def save_rules_to_list(rules):
    """
    Convert rules into a list of dictionaries.
    :param rules: List of tuples containing (rule, page_number).
    :return: List of dictionaries, each representing a field and its details.
    """
    rules_list = []
    for rule, page in rules:
        field_name, rule_description = rule.split(':', 1)
        rules_list.append({
            "fieldName": field_name.strip(),
            "rule": rule_description.strip(),
            "query": "",
            "pageNumber": page
        })
    return rules_list

# ========== 4. Main Pipeline Execution ==========
def main(pdf_path, api_key):
    print("Extracting page-wise text from PDF...")
    page_texts = extract_text_by_page(pdf_path)

    all_rules = []
    print("Generating rules using Groq LLM API...")
    for page_num, page_text in page_texts.items():
        rules = extract_rules_llm_groq(page_text, page_num, api_key)
        all_rules.extend(rules)

    print("Converting rules to list of dictionaries...")
    rules_list = save_rules_to_list(all_rules)

    # Push rules to MongoDB
    print("Pushing rules to MongoDB...")
    mongo_client = MongoClient("mongodb+srv://agastya2002:O9VgJkMJpdOFCShC@cluster0.wbyds.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Update with your MongoDB connection string if needed
    mongo_service = BaseMongoService(mongo_client, "Test_Rules")
    mongo_service.create_many(rules_list)  # Wrap the list in a dictionary for MongoDB

    print("✅ Audit rule extraction complete and saved to MongoDB!")
    return rules_list


input_pdf = "/Users/agastya/Documents/Projects/gaidp-l-la-ma-mia/code/src/backend/poc/extracted_part.pdf"  # Update if needed
groq_api_key = os.getenv("GROQ_API_KEY")  # Set your Groq API key as environment variable
if not groq_api_key:
    print("❌ ERROR: Please set your Groq API key as an environment variable 'GROQ_API_KEY'")
else:
    rules_list = main(input_pdf, groq_api_key)
    print(rules_list)  # Print or use the dictionary as needed
