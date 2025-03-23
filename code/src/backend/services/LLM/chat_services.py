import re
import requests
import os 

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

def update_rules(update_condition, api_key=os.environ.get('GROQ_API_KEY'), model='llama-3.3-70b-versatile'):
    """
    Updates the rules in the database with the given rule.

    Args:
        rule (dict): {constraint: str, mongo_query: str}
    """
    

    field = extract_word_after_hash(update_condition)
    if field is None:
        return Exception("No field provided in the update condition.")
    
    # get rule from DB TODO but for now read json
    import json
    json_file_path = '/Users/parthshukla/Documents/_working_space/gaidp-l-la-ma-mia/code/src/backend/poc/mongo_queries_output.json'
    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise Exception(f"JSON file not found at path: {json_file_path}")
    except json.JSONDecodeError:
        raise Exception("Error decoding JSON file.")

    data = {}
    for rule in json_data:
        if field.upper() in rule['constraint'].upper():
            data = rule
            break
    if not data:
        return Exception("No rule found for the given field.")
    print('------------')
    print(data)
    print('------------')
    
    if not api_key:
        return Exception("No Groq API key found.")
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
            {"role": "user", "content": f'Following is the existing rule: {data} User wants to: {update_condition.replace("#", "")}'}
        ],
        "temperature": 0.8,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=rules_payload)
    if response.status_code == 200:
        result = response.json()
        output_text = result['choices'][0]['message']['content']

        # Clean up the JSON-like string and convert it to a Python dictionary
        try:
            print(f"Updated rule as JSON-like string: {output_text}")
            cleaned_json = output_text.strip('```json\n').strip('```')  # Remove the ```json and ``` markers
            updated_rule = json.loads(cleaned_json)  # Convert to Python dictionary
            print(f"Updated rule as Python dict: {updated_rule}")
            return updated_rule
        except json.JSONDecodeError:
            raise Exception("Failed to parse the JSON response from the API.")
    else:
        print(f"Error from Groq API while updating rule:", response.text)
        return {}
    
if __name__=='__main__':
    print('Modify #Segment_id to accept 13 digit numbers as well')
    update_rules('Modify #Segment_id to accept 13 digit numbers as well')