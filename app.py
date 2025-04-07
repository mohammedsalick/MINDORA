from flask import Flask, request, jsonify, render_template, redirect, session
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Required for session management

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Gemini API details
GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_gemini_response(user_input, username="User", conversation_history=[]):
    headers = {
        "Content-Type": "application/json"
    }

    # Debug prints
    print(f"API URL being used: {GEMINI_API_URL}")

    prompt = f"""
    You are a mental health support chatbot. Help {username} who is facing {user_input}. 
    Be empathetic, supportive, and ask questions to understand their situation better.
    Here is the conversation history so far:
    {conversation_history}

    Always respond as MINDORA and avoid repeating the user's name unnecessarily.
    Keep your responses concise and natural.
    """

    # Notice we're NOT specifying the model in the data
    # The model is already in the URL from the .env file
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Sorry, there was an error processing your request. Status code: {response.status_code}. Details: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"
@app.route("/home")
def home():
    return render_template("home.html")  # Serve home.html for non-logged-in users


@app.route("/")
def index():
    if 'user' not in session:
        return redirect("/home")
    
    # Fetch the user's metadata from Supabase
    user_response = supabase.auth.get_user()
    if user_response and hasattr(user_response, 'user'):
        name = user_response.user.user_metadata.get("name", "User")
    else:
        name = "User"
    
    return render_template("index.html", name=name)



@app.route("/get-chat/<chat_id>", methods=["GET"])
def get_chat(chat_id):
    try:
        # Fetch the chat by ID
        result = supabase.table("chats").select("*").eq("id", chat_id).execute()
        if result.data:
            return jsonify(result.data[0])
        else:
            return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        print(f"Error fetching chat: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message")
        is_new_chat = request.json.get("is_new_chat", False)
        chat_id = request.json.get("chat_id")

        print(f"Received chat_id: {chat_id}, is_new_chat: {is_new_chat}")  # Debugging

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Fetch the user's name and ID from Supabase
        user_response = supabase.auth.get_user()
        if user_response and hasattr(user_response, 'user'):
            user_id = user_response.user.id
            username = user_response.user.user_metadata.get("name", "User")
        else:
            print("User not authenticated")
            return jsonify({"error": "User not authenticated"}), 401

        # Fetch the latest chat from Supabase
        conversation_history = []
        if not is_new_chat and chat_id:
            result = supabase.table("chats").select("chats").eq("id", chat_id).execute()
            if result.data:
                conversation_history = result.data[0].get("chats", [])
            else:
                print("Chat not found")
                # If the chat ID is invalid, treat it as a new chat instead of returning an error
                is_new_chat = True
        else:
            # If no chat_id is provided or explicitly marked as new chat
            is_new_chat = True

        # Get bot response
        bot_response = get_gemini_response(user_input, username, conversation_history)
        conversation_history.append({"user": user_input, "bot": bot_response})

        # Store or update chat in Supabase
        if is_new_chat:
            result = supabase.table("chats").insert({
                "user_id": user_id,
                "name": username,
                "chats": conversation_history
            }).execute()
            chat_id = result.data[0]["id"]
        else:
            # Make sure chat_id is not None before using it
            if chat_id:
                supabase.table("chats").update({
                    "chats": conversation_history
                }).eq("id", chat_id).execute()
            else:
                # Handle the case where chat_id is None but is_new_chat is False
                result = supabase.table("chats").insert({
                    "user_id": user_id,
                    "name": username,
                    "chats": conversation_history
                }).execute()
                chat_id = result.data[0]["id"]

        return jsonify({"response": bot_response, "history": conversation_history, "chat_id": chat_id})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500  # Return the actual error message
@app.route("/new-chat", methods=["POST"])
def new_chat():
    try:
        # Fetch the user's ID from Supabase
        user_response = supabase.auth.get_user()
        if user_response and hasattr(user_response, 'user'):
            user_id = user_response.user.id
            username = user_response.user.user_metadata.get("name", "User")
        else:
            return jsonify({"error": "User not authenticated"}), 401

        # Create a new chat entry in Supabase
        result = supabase.table("chats").insert({
            "user_id": user_id,
            "name": username,
            "chats": []
        }).execute()

        return jsonify({"success": True, "chat_id": result.data[0]["id"]})
    except Exception as e:
        print(f"Error creating new chat: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/get-chats", methods=["GET"])
def get_chats():
    try:
        # Fetch the user's ID from Supabase
        user_response = supabase.auth.get_user()
        if user_response and hasattr(user_response, 'user'):
            user_id = user_response.user.id
        else:
            return jsonify({"error": "User not authenticated"}), 401

        # Fetch all chats for the user
        result = supabase.table("chats").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return jsonify(result.data)
    except Exception as e:
        print(f"Error fetching chats: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            # Sign in with Supabase
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            
            # Extract user data from the AuthResponse object
            user = auth_response.user
            if user:
                # Store user data in the session
                session['user'] = {
                    'id': user.id,
                    'email': user.email,
                    'name': user.user_metadata.get("name", "User")
                }
                return redirect("/")
            else:
                return render_template("login.html", error="Invalid credentials")
        except Exception as e:
            return render_template("login.html", error=str(e))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        name = request.form.get("name")

        # Validate input fields
        if not email or not password or not confirm_password or not name:
            return render_template("register.html", error="Please fill in all fields.")

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match.")

        try:
            # Sign up with Supabase and include additional user metadata
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "name": name
                    }
                }
            })

            # Check if registration was successful
            if auth_response.user:
                return redirect("/login")
            else:
                return render_template("register.html", error="Registration failed.")
        except Exception as e:
            return render_template("register.html", error=str(e))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)