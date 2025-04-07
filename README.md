![WhatsApp Image 2025-01-22 at 16 56 23_1fc51ed3](https://github.com/user-attachments/assets/ca1e612a-b80f-4ac1-9748-231d1d68f83f)# MINDORA: Mental Health Support Chatbot

MINDORA is a Flask-based chatbot designed to provide empathetic and supportive responses for mental health support. It utilizes Supabase for user authentication and chat storage and integrates Gemini API for generating natural language responses.

## Features
- User authentication (Login and Registration).
- Real-time chat with personalized responses.
- Conversation history saved in Supabase.
- Lightweight Flask server.

---

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Environment Variables](#environment-variables)
3. [Run the Application](#run-the-application)
4. [Using the Application](#using-the-application)
5. [Contributing](#contributing)
6. [License](#license)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/mohammedsalick/MINDORA.git
cd MINDORA
```

### 2. Install Dependencies
Ensure you have Python installed on your machine.

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add the following:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GEMINI_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=your_flask_secret_key
```
Replace `your_supabase_url`, `your_supabase_key`, `your_gemini_api_key`, and `your_flask_secret_key` with your actual credentials.

---

## Run the Application

Start the Flask server using:
```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

---

## Using the Application

1. Navigate to `http://127.0.0.1:5000/home` to access the home page.
2. Register a new account or log in with an existing account.
3. Begin chatting with MINDORA. All chat histories will be stored securely in Supabase.

---

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For any queries or issues, please feel free to open an issue in the repository or contact me at mhmmdsalick@gmail.com .
![WhatsApp Image 2025-01-22 at 16 56 23_7533119c](https://github.com/user-attachments/assets/cc0be4cd-da9a-4e34-aeee-546ecfb110bc)
![WhatsApp Image 2025-01-22 at 16 57 16_9b8a290b](https://github.com/user-attachments/assets/cc5e4420-3358-4f5b-a1bd-77a3d7b4b0da)
![WhatsApp Image 2025-01-22 at 16 52 36_020a1e61](https://github.com/user-attachments/assets/9a9d230c-36cd-4785-bb60-1b2385cf107b)



