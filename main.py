import os
import google.generativeai as genai
from flask import Flask, request, render_template

app = Flask(__name__)

# --- Configure Gemini API ---
# Ensure your API key is stored securely in Replit's "Secrets"
# Key: GOOGLE_API_KEY
# Value: Your actual Gemini API Key
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please add your Gemini API key as a secret in Replit (padlock icon).")
    exit(1)

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def index():
    explanation_text = ""
    if request.method == 'POST':
        user_topic = request.form['topic']
        if user_topic:
            try:
                # --- Customized Prompt for KNEC DICT Module 3 ---
                prompt = f"""
                You are an AI tutor specializing in the KNEC Diploma in Information Communication Technology (DICT) Module 3 syllabus.
                Your task is to provide a clear, concise, and relevant explanation for the following topic, as it pertains to the KNEC DICT Module 3 curriculum.
                Focus on core concepts and practical understanding. Avoid unnecessary jargon where simpler terms suffice.
                Do not escape characters like <, >, &, etc.
                Format the code properly, with indentation and line breaks where appropriate.

                Topic for explanation: "{user_topic}"
                """

                gemini_response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3, # A slightly higher temperature than fact-checking for more comprehensive answers
                        max_output_tokens=2000, # Increased output tokens for more detailed explanations
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )
                explanation_text = gemini_response.text
            except Exception as e:
                explanation_text = f"An error occurred: {e}. Please try again later. (API usage limits?) Ensure your topic is appropriate."
        else:
            explanation_text = "Please enter a topic to get an explanation."

    return render_template('index.html', explanation=explanation_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))