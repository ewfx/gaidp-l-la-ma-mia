import json
import re
import requests
import os 
from pymongo import MongoClient
from services.base_mongo_service import BaseMongoService
from services.utils import get_available_api_key


def extract_word_after_hash(input_string):
    """
    Extracts the word immediately following the '#' symbol in the input string.

    Args:
        input_string (str): The input string to search.

    Returns:
        str: The word following the '#' symbol, or None if no match is found.
    """
    match = re.search(r"#(\w+)", input_string)
    return match.group(1) if match else None

def update_rules(update_condition, pdfName, schedule, category, api_key='', model='llama-3.3-70b-versatile'):
    """
    Updates the rules in the database with the given rule.

    Args:
        update_condition (str): The condition to modify the rule.
        pdfName (str): The name of the PDF.
        schedule (str): The schedule name.
        category (str): The category name.
    """
    api_key = get_available_api_key()
    field = extract_word_after_hash(update_condition)
    if field is None:
        raise Exception("No field provided in the update condition.")
    
    # Remove the .pdf extension from pdfName
    sanitized_pdf_name = re.sub(r'\.pdf$', '', pdfName, flags=re.IGNORECASE)

    # Generate the sanitized collection name
    collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
    collection_name = re.sub(r'[^a-zA-Z0-9_]', '', collection_name)  # Keep only alphanumeric characters and underscores

    # Fetch the rule and query from the database
    mongo_client = MongoClient(os.environ.get("MONGO_URI"))  # Replace with your MongoDB connection string
    mongo_service = BaseMongoService(mongo_client, collection_name)
    rule_data = mongo_service.find_one({"fieldName": field})

    if not rule_data:
        raise Exception("No rule found for the given field.")
    
    print('------------')
    print(rule_data)
    print('------------')
    
    if not api_key:
        raise Exception("No Groq API key found.")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    system_prompt = '''You are an expert at understanding auditing rules and writing MongoDB queries. I will provide you a json that contains current rule and its supporting query. I will also provide you with a modifying statement, you need to update the rule and supporting query. You are only allowed to return a json with updated rule and supporting query.'''
    rules_payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f'Following is the existing rule: {rule_data} User wants to: {update_condition.replace("#", "")}. Make sure to give the mongo query in a python dictionary like format. Dont add any escape sequnces.'}
        ],
        "temperature": 0.8,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=rules_payload)
    if response.status_code == 200:
        result = response.json()
        output_text = result['choices'][0]['message']['content']
        print(type(output_text))
        # Clean up the JSON-like string and convert it to a Python dictionary
        try:
            print(f"Updated rule as JSON-like string: {output_text}")
            cleaned_json = output_text.strip('```json\n').strip('```').replace("False", "false").replace("True", "true").replace("None", "null")  # Remove the ```json and ``` markers
            print(f"Cleaned JSON-like string: {cleaned_json}")
            updated_rule = json.loads(cleaned_json)  # Convert to Python dictionary
            print(f"Updated rule as Python dict: {updated_rule}")
            return updated_rule
        except json.JSONDecodeError:
            raise Exception("Failed to parse the JSON response from the API.")
    else:
        print(f"Error from Groq API while updating rule:", response.text)
        return {}
    
# if __name__=='__main__':
#     print('Modify #SEGMENT_ID to accept 13 digit numbers as well')
#     update_rules('Modify #Segment_id to accept 13 digit numbers as well')