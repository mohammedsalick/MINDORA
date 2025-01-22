from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# Gemini API details
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
GEMINI_API_KEY = "AIzaSyBwJavDZUC02-o7tQn2UYcGZfhSf5fmaGw"  # Replace with your actual API key

def get_gemini_response(user_input, username="User", conversation_history=[]):
    """
    Send user input to the Gemini API and get the chatbot's response.
    The chatbot will ask questions and guide the user to reframe their thoughts.
    """
    headers = {
        "Content-Type": "application/json"
    }

    # Contextual prompt for mental health support
    prompt = f"""
    You are a mental health support chatbot. Your goal is to help {username} who is facing {user_input}. 
    Ask open-ended questions to understand their situation better and guide them to reframe their thoughts.
    Be empathetic, supportive, and avoid providing direct answers. Instead, help them discover solutions on their own.
    Here is the conversation history so far:
    {conversation_history}
    """

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
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
    username = request.json.get("username", "User")  # Default to "User" if no username is provided
    conversation_history = request.json.get("history", [])  # Get conversation history

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Add the user's message to the conversation history
    conversation_history.append(f"{username}: {user_input}")

    # Get response from Gemini API
    bot_response = get_gemini_response(user_input, username, conversation_history)

    # Add the bot's response to the conversation history
    conversation_history.append(f"Chatbot: {bot_response}")

    return jsonify({"response": bot_response, "history": conversation_history})

if __name__ == "__main__":
    app.run(debug=True)