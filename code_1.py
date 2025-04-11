from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from openai import OpenAI

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# ✅ Initialize OpenAI client (Make sure your key is valid and not expired)
client = OpenAI(api_key="insert your actual key ")  # ← insert your actual key here

@app.route('/analyze', methods=['POST'])
def analyze_content():
    data = request.json
    content = data.get('content', '')

    if not content:
        return jsonify({"error": "No content provided"}), 400

    result = analyze_text(content)

    if 'error' in result:
        return jsonify(result), 500

    return jsonify(result)

def analyze_text(text):
    prompt = f"""
    Analyze the following content and return a JSON object with:
    - sentiment: positive, negative, or neutral
    - bias: biased, non-biased, or neutral
    - credibility_score: a number between 0 and 1

    Content:
    {text}

    Respond ONLY with a JSON object like:
    {{
        "sentiment": "...",
        "bias": "...",
        "credibility_score": 0.87
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a credibility analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        reply = response.choices[0].message.content.strip()

        # Parse response as JSON
        return json.loads(reply)

    except Exception as e:
        return {
            "error": "Failed to analyze content",
            "details": str(e)
        }

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
