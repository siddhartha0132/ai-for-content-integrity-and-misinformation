from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_content():
    data = request.json  # Get the JSON input data
    content = data.get('content', '')
    
    if not content:
        return jsonify({"error": "No content provided"}), 400
    
    # Placeholder function to analyze the content (we'll fill this in later)
    credibility_score = analyze_text(content)
    
    return jsonify({"credibility_score": credibility_score})

def analyze_text(text):
    # This will be the function where we analyze the text and provide a score
    return "placeholder_score"  # Replace this later with actual logic

if __name__ == '__main__':
    app.run(debug=True)

from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
    return sentiment_score


from transformers import pipeline

# Load Hugging Face model for bias detection (sentiment or other tasks)
bias_model = pipeline('zero-shot-classification', model="facebook/bart-large-mnli")

def analyze_bias(text):
    candidate_labels = ["bias", "neutral", "non-bias"]
    result = bias_model(text, candidate_labels=candidate_labels)
    return result['labels'][0]  # Return the label with the highest score


from newsapi import NewsApiClient

# Initialize NewsAPI client (you need an API key from https://newsapi.org/)
newsapi = NewsApiClient(api_key='YOUR_API_KEY')

def fact_check_article(title):
    # Query the news API for related articles
    response = newsapi.get_everything(q=title, language='en')
    articles = response.get('articles', [])
    
    if articles:
        return True  # Fact-checked information is found
    return False

def analyze_text(text):
    sentiment_score = analyze_sentiment(text)
    bias_score = analyze_bias(text)
    
    # Use the article title or content for fact-checking
    fact_check_status = fact_check_article(text[:30])  # Taking first 30 chars as a title example
    
    # Calculate credibility score
    credibility_score = calculate_credibility(sentiment_score, bias_score, fact_check_status)
    
    return credibility_score

def calculate_credibility(sentiment, bias, fact_checked):
    # Here, you can combine scores. For simplicity:
    score = 0
    
    # Sentiment score (-1 to 1)
    score += sentiment * 0.4
    
    # Bias score (e.g., 'bias', 'neutral', 'non-bias')
    if bias == "bias":
        score -= 0.4  # Penalize if biased
    elif bias == "neutral":
        score += 0.2  # Reward neutral content
    
    # Fact-check status
    if not fact_checked:
        score -= 0.2  # Penalize if no fact-checking is found
    
    # Return the final score (normalized between 0 and 1)
    return max(0, min(1, score))

@app.route('/analyze', methods=['POST'])
def analyze_content():
    data = request.json  # Get the JSON input data
    content = data.get('content', '')
    
    if not content:
        return jsonify({"error": "No content provided"}), 400
    
    # Analyze text using all methods
    credibility_score = analyze_text(content)
    
    return jsonify({"credibility_score": credibility_score})

if __name__ == '__main__':
    app.run(debug=True)