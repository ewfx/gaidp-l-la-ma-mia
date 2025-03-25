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
from io import BytesIO
import re  # Import regex for sanitizing collection names

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
def extract_profiling_rules(pdf_name, schedule, category):
    """
    Extract profiling rules for a specific category in a schedule from a PDF stored in MongoDB.

    Args:
        pdf_name (str): The name of the PDF.
        schedule (str): The schedule name.
        category (str): The category name.

    Returns:
        list: A list of dictionaries containing the extracted rules.
    """
    try:
        # Initialize MongoDB client and collections
        mongo_client = MongoClient(os.environ.get("MONGO_URI"))  # Replace with your MongoDB connection string
        db = mongo_client["DataProfiling"]
        pdf_index_collection = db["PDF_Index"]
        raw_pdfs_collection = db["Raw_PDFs"]

        # Fetch the page range for the given schedule and category from PDF_Index
        pdf_index_record = pdf_index_collection.find_one({"Name": pdf_name})
        if not pdf_index_record:
            raise ValueError(f"PDF index for '{pdf_name}' not found in the database.")

        schedule_data = next((s for s in pdf_index_record["Schedules"] if s["Name"] == schedule), None)
        if not schedule_data:
            raise ValueError(f"Schedule '{schedule}' not found in the PDF index.")

        category_data = next((c for c in schedule_data["Categories"] if c["Name"] == category), None)
        if not category_data:
            raise ValueError(f"Category '{category}' not found in the schedule '{schedule}'.")

        start_page = category_data["Page"]

        # Determine end_page from the next category in the schedule
        categories = schedule_data["Categories"]
        current_index = categories.index(category_data)
        end_page = categories[current_index + 1]["Page"] if current_index + 1 < len(categories) else start_page

        # Fetch the PDF blob from Raw_PDFs
        pdf_record = raw_pdfs_collection.find_one({"name": pdf_name})
        if not pdf_record:
            raise ValueError(f"PDF with name '{pdf_name}' not found in the database.")

        pdf_blob = pdf_record["pdf_blob"]

        # Load the PDF from the blob and extract relevant pages
        pdf_stream = BytesIO(pdf_blob)
        page_texts = {}
        with pdfplumber.open(pdf_stream) as pdf:
            for page_num in range(start_page - 1, end_page - 1):  # Convert to zero-based index
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    page_texts[page_num + 1] = text  # Convert back to one-based index

        # Extract rules using Groq LLM API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        all_rules = []
        for page_num, page_text in page_texts.items():
            rules = extract_rules_llm_groq(page_text, page_num, api_key)
            all_rules.extend(rules)

        # Convert rules to list of dictionaries
        rules_list = save_rules_to_list(all_rules)

        # Remove the .pdf extension from pdf_name
        sanitized_pdf_name = re.sub(r'\.pdf$', '', pdf_name, flags=re.IGNORECASE)

        # Sanitize the collection name by removing spaces and special characters
        collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
        collection_name = re.sub(r'[^a-zA-Z0-9_]', '', collection_name)  # Keep only alphanumeric characters and underscores
        # Push rules to MongoDB
        mongo_service = BaseMongoService(mongo_client, collection_name)
        mongo_service.create_many(rules_list)

    except Exception as e:
        raise ValueError(f"Failed to extract profiling rules: {str(e)}")

