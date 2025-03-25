import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_available_api_key(test_endpoint="https://api.groq.com/openai/v1/chat/completions"):
    """
    Attempts to use API keys stored in the environment variables
    with the pattern GROQ_API_KEY1, GROQ_API_KEY2, etc., and returns
    the first available key that does not result in a rate-limit error.

    Args:
        test_endpoint (str): The endpoint to test the API key.

    Returns:
        str: The available API key.
    Raises:
        Exception: If no valid API key is available.
    """
    api_key_pattern = "GROQ_API_KEY_"
    index = 1

    while True:
        api_key_env = f"{api_key_pattern}{index}"
        api_key = os.getenv(api_key_env)  # Use dotenv to fetch the environment variable

        if not api_key:
            break  # No more keys to check

        # Test the current API key by making a request to the Chat Completion endpoint
        try:
            payload = {
                "model": "llama-3.3-70b-versatile",  # Replace with the appropriate model name
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5,
            }
            response = requests.post(
                test_endpoint,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json=payload,
            )

            if response.status_code == 200:
                print(f"API key {api_key_env} is valid and available.")
                return api_key  # Return the first available key
            elif response.status_code == 429:  # HTTP 429 Too Many Requests
                print(f"API key {api_key_env} has exceeded its rate limit.")
            else:
                print(f"API key {api_key_env} is invalid or returned status {response.status_code}.")
        except Exception as e:
            print(f"Error testing API key {api_key_env}: {e}")

        index += 1

    raise Exception("No valid API key is available.")