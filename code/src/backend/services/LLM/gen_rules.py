import os
import pdfplumber
import csv
import requests

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

    output_format = '''{"columnName": <string>,"description": <string>,"rules": [{"rule": <string>,"query": <string>}],"foreignRules": [{"rule": <string>,"query": <string>}]}'''

    prompt = f"Extract data profiling rules from the following text for all variables / fields, make sure to only have 'variable : comma-separated rules' and no other extra text. Further where there are fixed values possible, mention that in the description :\n\n{page_text}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an expert in understanding audit rules. You can read through a bunch of text and figure out the variables / fields in the data and the meaning of each field. You can translate the long descriptions into simple data profiling rules. Avoid putting $ and # in the output. Put them in the format: {output_format}"},
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


# ========== 3. Save Rules to CSV ==========
def save_rules_to_csv(rules, output_file='audit_rules_groq_api.csv'):
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Field', 'Rule', 'Page Number'])
        for rule, page in rules:
            field = rule.split(':')[0].strip()
            rule = rule.split(':')[1].strip()
            writer.writerow([field, rule, page])


# ========== 4. Main Pipeline Execution ==========
def gen_rules(pdf_path, api_key):
    print("Extracting page-wise text from PDF...")
    page_texts = extract_text_by_page(pdf_path)

    all_rules = []
    print("Generating rules using Groq LLM API...")
    for page_num, page_text in page_texts.items():
        rules = extract_rules_llm_groq(page_text, page_num, api_key)
        all_rules.extend(rules)

    print("Saving rules to CSV file...")
    save_rules_to_csv(all_rules)
    print("✅ Audit rule extraction complete! Output saved to 'audit_rules_groq_api.csv'.")


# ========== 5. Run ==========
if __name__ == "__main__":
    input_pdf = "/Users/parthshukla/Documents/_working_space/gaidp-l-la-ma-mia/code/src/backend/poc/extracted_part.pdf"  # Update if needed
    groq_api_key = os.getenv("GROQ_API_KEY")  # Set your Groq API key as environment variable
    if not groq_api_key:
        print("❌ ERROR: Please set your Groq API key as an environment variable 'GROQ_API_KEY'")
    else:
        gen_rules(input_pdf, groq_api_key)