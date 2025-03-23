# audit_rule_extractor_groq.py

"""
LLM-based Audit Rule Extractor for PDF Documents using Groq.com API (e.g., Mixtral or LLaMA3)
Requires a free Groq API key
"""

import os
import pdfplumber
import csv
import requests

# ========== 1. Load PDF and Extract All Text ==========
def extract_all_text(pdf_path):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                all_text.append((i, text))
    return all_text


# ========== 2. Extract Data Elements and Rules Using Groq API ==========
def extract_data_elements_and_rules(all_text, api_key, model="llama-3.3-70b-versatile"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    combined_text = "\n\n".join([f"Page {page_num}:\n{text}" for page_num, text in all_text])
    
    # Prompt to extract data elements
    data_elements_prompt = f"Identify all data elements mentioned in the following text. Provide a list of unique data elements:\n\n{combined_text}"

    # Payload for extracting data elements
    data_elements_payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in identifying data elements from text."},
            {"role": "user", "content": data_elements_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    # API call to extract data elements
    response = requests.post(url, headers=headers, json=data_elements_payload)
    if response.status_code == 200:
        result = response.json()
        output_text = result['choices'][0]['message']['content']
        data_elements = [line.strip('-• ') for line in output_text.split('\n') if len(line.strip()) > 0]
        print(f"Extracted data elements: {data_elements}")
    else:
        print(f"Error from Groq API while extracting data elements:", response.text)
        return {}, []

    # Prompt to extract rules for all data elements
    rules_prompt = f"Extract data profiling rules from the following text for all the identified data elements: {', '.join(data_elements)}. Make sure to only have 'variable : comma-separated rules' and no other extra text. Further where there are fixed values possible, mention that in the description:\n\n{combined_text}"

    # Payload for extracting rules
    rules_payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in understanding audit rules. You can read through a bunch of text and figure out the variables / fields in the data and the meaning of each field. You can translate the long descriptions into simple data profiling rules."},
            {"role": "user", "content": rules_prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 3000
    }

    # API call to extract rules
    response = requests.post(url, headers=headers, json=rules_payload)
    if response.status_code == 200:
        result = response.json()
        output_text = result['choices'][0]['message']['content']
        rules_by_data_element = {}
        for line in output_text.split('\n'):
            if ':' in line:
                data_element, rules = line.split(':', 1)
                rules_by_data_element[data_element.strip()] = [rule.strip() for rule in rules.split(',')]
        return rules_by_data_element, data_elements
    else:
        print(f"Error from Groq API while extracting rules:", response.text)
        return {}, []


# ========== 3. Save Rules to CSV ==========
def save_rules_to_csv(rules_by_data_element, output_file='audit_rules_by_data_element.csv'):
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Data Element', 'Rule'])
        for data_element, rules in rules_by_data_element.items():
            for rule in rules:
                writer.writerow([data_element, rule])


# ========== 4. Main Pipeline Execution ==========
def main(pdf_path, api_key):
    print("Extracting all text from PDF...")
    all_text = extract_all_text(pdf_path)

    print("Extracting data elements and rules using Groq API...")
    rules_by_data_element, data_elements = extract_data_elements_and_rules(all_text, api_key)

    if not data_elements:
        print("No data elements identified. Exiting.")
        return

    print("Saving rules to CSV file...")
    save_rules_to_csv(rules_by_data_element)
    print("✅ Audit rule extraction complete! Output saved to 'audit_rules_by_data_element.csv'.")


# ========== 5. Run ==========
if __name__ == "__main__":
    input_pdf = "extracted_part.pdf"  # Update if needed
    groq_api_key = os.getenv("GROQ_API_KEY")  # Set your Groq API key as environment variable
    if not groq_api_key:
        print("❌ ERROR: Please set your Groq API key as an environment variable 'GROQ_API_KEY'")
    else:
        main(input_pdf, groq_api_key)
