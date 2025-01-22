from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# Gemini API details
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
GEMINI_API_KEY = "AIzaSyBwJavDZUC02-o7tQn2UYcGZfhSf5fmaGw"  # Replace with your actual API key

def get_gemini_response(user_input):
    """
    Send user input to the Gemini API and get the chatbot's response.
    """
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": user_input}
                ]
            }
        ]
    }
    # Add API key as a query parameter
    params = {
        "key": GEMINI_API_KEY
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data, params=params)
    if response.status_code == 200:
        # Extract the response text from the API's JSON response
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Sorry, there was an error processing your request. Status code: {response.status_code}"

@app.route("/")
def index():
    """
    Serve the index.html file.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint to handle user messages and return chatbot responses.
    """
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get response from Gemini API
    bot_response = get_gemini_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)