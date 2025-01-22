# chatbot.py
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBwJavDZUC02-o7tQn2UYcGZfhSf5fmaGw")

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro')

def interact(username, issue, message=None):
    if message:
        prompt = f"{username} says: {message}. You are a mental health support chatbot. Respond empathetically."
    else:
        prompt = f"You are a mental health support chatbot. Help {username} who is facing {issue}. Be empathetic and supportive."

    # Generate response using Gemini
    response = model.generate_content(prompt)
    return response.text