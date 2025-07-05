import os
import google.generativeai as genai
from flask import Flask, request, render_template
import markdown
from markupsafe import Markup


app = Flask(__name__)

# Configure Gemini API
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please add your Gemini API key as a secret (e.g., in a .env file locally or Replit Secrets if deploying).")
    exit(1)

# Initializing the Gemini Pro model
model = genai.GenerativeModel('gemini-1.5-flash')


@app.route('/', methods=['GET', 'POST'])
def index():
    explanation_text = ""
    user_topic = ""

    if request.method == 'POST':
        user_topic = request.form['user_topic']
        if user_topic:
            try:
                # --- Prompt for Clean, Readable KNEC DICT Module 3 Responses ---
                prompt = f"""
                You are an elite AI mentor and KNEC DICT Module 3 expert with deep technical knowledge and the ability to make complex concepts crystal clear.
                Your mission: Provide an intelligent, engaging, and comprehensive explanation that demonstrates mastery of the topic while being accessible to students.
                ❗IMPORTANT:
                You are ONLY allowed to answer questions related to KNEC DICT Module 3 (Diploma in Information Communication Technology).
                If a user asks anything unrelated — such as Biology, Chemistry, Cooking, Politics, or anything outside ICT — politely respond with:
                "I'm only trained to answer questions related to ICT topics in the KNEC Module 3 syllabus. Please ask something related to web development, networking, programming, databases, or software engineering."

                DO NOT answer questions unrelated to the KNEC DICT syllabus.


                📋 RESPONSE STRUCTURE:
                1. Start with a brief, punchy definition or overview.
                2. Break down key concepts with clear explanations.
                3. Include COMPLETE, RUNNABLE code examples with full implementations (if applicable to the topic).
                4. Add practical real-world applications and use cases.
                5. Include useful tips, best practices, or "pro insights".
                6. End with a quick summary or key takeaway.

                🎯 FORMATTING GUIDELINES - VERY IMPORTANT:
                - Use proper Markdown for all formatting.
                - Headings: Use # for H1, ## for H2, ### for H3.
                - Bold: Use **double asterisks** for bolding (e.g., **important term**).
                - Italic: Use *single asterisks* for italics (e.g., *key concept*).
                - Lists: Use `*` or `-` for unordered lists, and `1.` `2.` for ordered lists.
                - Use clear, professional paragraphs.
                - Add relevant emojis sparingly for visual appeal.
                💡 Pro Tip: For expert insights.
                🎯 Key Takeaway: For summaries.
                ⭐ Important: For critical points.

                💻 CODE EXAMPLES - CRITICAL REQUIREMENTS:
                - Provide COMPLETE, RUNNABLE code examples ONLY WHEN THE TOPIC INVOLVES PROGRAMMING or would clearly benefit from practical implementation.
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

                # Converting Markdown to HTML for display
                md = markdown.Markdown(
                    extensions=['codehilite', 'fenced_code', 'tables', 'extra']
                )
                explanation_text = Markup(md.convert(raw_text))

            except Exception as e:
                
                explanation_text = f"An error occurred: {e}. Please try again later. (API usage limits?) Ensure your topic is appropriate."
        else:
            explanation_text = "Please enter a topic to get an explanation."

    return render_template('index.html', explanation=explanation_text, topic=user_topic)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # local development & deployment port
    app.run(host='0.0.0.0', port=port)
