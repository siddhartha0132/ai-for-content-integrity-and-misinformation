import requests
import json

# URL of the Flask backend endpoint
url = "http://127.0.0.1:5000/analyze"

# Example content to test
test_content = {
    "content": "This is a neutral statement with no bias or misleading information."
}

# Send POST request to the Flask backend with the test content
response = requests.post(url, json=test_content)

# Check if the request was successful and print the response
if response.status_code == 200:
    result = response.json()  # Get the JSON response
    print("Credibility Score:", result.get("credibility_score"))
else:
    print("Error:", response.status_code, response.text)
