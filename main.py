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
                # --- Enhanced Prompt for Clean, Readable KNEC DICT Module 3 Responses ---
                prompt = f"""
                You are an elite AI mentor and KNEC DICT Module 3 expert with deep technical knowledge and the ability to make complex concepts crystal clear.
                
                Your mission: Provide an intelligent, engaging, and comprehensive explanation that demonstrates mastery of the topic while being accessible to students.
                
                📋 RESPONSE STRUCTURE:
                1. Start with a brief, punchy definition or overview
                2. Break down key concepts with clear explanations
                3. Include practical examples or real-world applications
                4. Add useful tips, best practices, or "pro insights"
                5. End with a quick summary or key takeaway
                
                🎯 FORMATTING GUIDELINES - VERY IMPORTANT:
                - DO NOT use asterisks (*) around words for emphasis or bold formatting
                - Use plain text with clear, readable language
                - For key terms, simply write them naturally without any special formatting
                - Use relevant emojis sparingly for visual appeal
                - Format with clean listing styles:
                  • Start bullet points with simple text
                  • Use indentation with spaces for sub-points
                  • Use "💡 Pro Tip:" for expert insights
                  • Use "🎯 Key Takeaway:" for summaries
                  • Use "⭐ Important:" for critical points
                
                EXAMPLES OF GOOD FORMATTING:
                ✅ Layer 1: Network Access Layer
                ❌ **Layer 1: Network Access Layer:**
                
                ✅ This handles physical transmission
                ❌ This **handles** physical transmission
                
                - Write in clear, professional paragraphs
                - Use proper headings (# ## ###) when needed
                - Add code examples with proper syntax when relevant
                - Use analogies to make complex concepts relatable
                - Include industry terminology but explain it clearly
                
                💡 Make it sound like advice from a seasoned tech professional who really knows their stuff, but keep the formatting clean and readable!
                
                Topic to explain: "{user_topic}"
                """

                gemini_response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.4, # Slightly higher for more engaging and dynamic responses
                        max_output_tokens=2500, # More tokens for comprehensive, well-structured responses
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