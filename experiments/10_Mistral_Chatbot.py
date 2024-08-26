import requests
from mistralai.exceptions import MistralAPIException

api_key = "1rg5xp5fhzzzoqaEXGRGsFvol9FpWtgx"
# base_url = "https://api.mistral.ai/v1"
# endpoint = "/chat/completions"

import requests

# api_key = "YOUR_API_KEY"
base_url = "https://api.mistral.ai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Example payload, replace with actual data as per Mistral API documentation
payload = {
  "model": "mistral-small-latest",
  "temperature": 0.7,
  "top_p": 1,
  "max_tokens": 0,
  "min_tokens": 0,
  "stream": False,
  "stop": "string",
  "random_seed": 0,
  "messages": [
    {
      "role": "user",
      "content": "Who is the best French painter? Answer in one short sentence."
    }
  ],
  "response_format": {
    "type": "text"
  },
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "string",
        "description": "",
        "parameters": {}
      }
    }
  ],
  "tool_choice": "auto",
  "safe_prompt": False
}

try:
    # Use 'json' parameter to automatically set Content-Length
    response = requests.post(base_url, headers=headers, json=payload)

    # Check if request was successful
    response.raise_for_status()
    data = response.json()
    print("Response from API:", data)

except requests.exceptions.HTTPError as http_err:
    if response.status_code == 411:
        print("Error: Content-Length header is required but missing.")
    else:
        print(f"HTTP error occurred: {http_err}")
except Exception as e:
    print(f"An error occurred: {e}")
