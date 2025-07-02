import os
import google.generativeai as genai
from flask import Flask, request, render_template
import markdown
from markupsafe import Markup # Needed for |safe filter

# Import SQLAlchemy only once
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# checks instance folder exists
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

# SQLite DB path
db_path = os.path.join(app.root_path, 'instance', 'revision_bot.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100)) # Consider making this dynamic (e.g., session ID) or removing if not used
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

# --- Configure Gemini API (MOVED TO TOP-LEVEL) ---
try:
    # Ensure GOOGLE_API_KEY is loaded from .env or system environment
    # from dotenv import load_dotenv # Uncomment if you're using .env locally
    # load_dotenv() # Uncomment if you're using .env locally

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please add your Gemini API key as a secret (e.g., in .env file or Replit Secrets).")
    exit(1)

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-1.5-flash')


@app.route('/', methods=['GET', 'POST'])
def index(): # Consolidated function
    explanation_text = ""
    user_topic = "" # Initialize user_topic for GET requests

    if request.method == 'POST':
        user_topic = request.form['user_topic'] # CORRECTED: Access 'user_topic' from form
        if user_topic:
            try:
                # --- Enhanced Prompt for Clean, Readable KNEC DICT Module 3 Responses ---
                prompt = f"""
                You are an elite AI mentor and KNEC DICT Module 3 expert with deep technical knowledge and the ability to make complex concepts crystal clear.

                Your mission: Provide an intelligent, engaging, and comprehensive explanation that demonstrates mastery of the topic while being accessible to students.

                📋 RESPONSE STRUCTURE:
                1. Start with a brief, punchy definition or overview
                2. Break down key concepts with clear explanations
                # 3. Include COMPLETE, RUNNABLE code examples with full implementations
                4. Add practical real-world applications and use cases
                5. Include useful tips, best practices, or "pro insights"
                6. End with a quick summary or key takeaway

                🎯 FORMATTING GUIDELINES - VERY IMPORTANT:
                - Use proper Markdown for all formatting.
                - Headings: Use # for H1, ## for H2, ### for H3.
                - Bold: Use **double asterisks** for bolding (e.g., **important term**).
                - Italic: Use *single asterisks* for italics (e.g., *key concept*).
                - Lists: Use `*` or `-` for unordered lists, and `1.` `2.` for ordered lists.
                - Use clear, professional paragraphs.
                - Add relevant emojis sparingly for visual appeal.
                - Examples of good formatting (ignore the previous negative examples you had, they contradict using markdown):
                  * This is a bullet point.
                  * This is another bullet point.
                  * This is a sub-point with indentation.
                💡 Pro Tip: For expert insights.
                🎯 Key Takeaway: For summaries.
                ⭐ Important: For critical points.

                💻 CODE EXAMPLES - CRITICAL REQUIREMENTS:
                - Provide COMPLETE, RUNNABLE code examples only when the topic involves programming or would clearly benefit from practical implementation.
                - Use Markdown fenced code blocks (```language\ncode\n```) for proper syntax highlighting.
                - Ensure code is production-ready and can be run directly by students.
                - Do not use code snippets with "..." or incomplete examples.
                - Always include necessary imports, declarations, and all required code.
                - Use clear, descriptive variable names and comments.
                - For Python, include a complete script with all imports.
                - For HTML/CSS, provide a complete, functional web page including all necessary tags (`<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`, `<style>`, `<script>`).
                - For database examples, include full schema and sample data.
                - Include full file contents, not snippets.
                - Add proper imports, declarations, and all necessary code.
                - Include multiple examples for different scenarios when relevant.
                - Add comments explaining each part of the code.
                - Show both basic and advanced implementations.
                - Include example inputs and expected outputs.
                - When showing HTML/CSS, provide complete, functional web pages.
                - For database examples, include full schema and sample data.

                Topic to explain: "{user_topic}"
                """

                gemini_response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.4,
                        max_output_tokens=5500,
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )
                raw_text = gemini_response.text

                # Convert Markdown to HTML
                # Note: The prompt is now explicitly asking for Markdown, so we revert
                # to using markdown.Markdown for conversion.
                md = markdown.Markdown(
                    extensions=['codehilite', 'fenced_code', 'tables', 'extra'] # Added 'extra' for more general Markdown features
                )
                explanation_text = Markup(md.convert(raw_text))

                # --- Database Storage ---
                # You can add a user ID here if you implement login/sessions
                new_question = Question(user="Guest", question=user_topic, answer=raw_text)
                db.session.add(new_question)
                db.session.commit()
                # --- End Database Storage ---

            except Exception as e:
                explanation_text = f"An error occurred: {e}. Please try again later. (API usage limits?) Ensure your topic is appropriate."
        else:
            explanation_text = "Please enter a topic to get an explanation."

    # Pass explanation_text and user_topic to the template
    return render_template('index.html', explanation=explanation_text, topic=user_topic)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensure tables are created when the app starts
    app.run(debug=True) # Run in debug mode for local development