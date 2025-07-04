# KNEC DICT Module 3 AI Tutor Bot

## Project Description

This project is an AI-powered web-based tutor designed specifically to assist students with the **KNEC Diploma in Information Communication Technology (DICT) Module 3 syllabus**. Built with Flask, this bot leverages the power of Google's Gemini 1.5 Flash model to provide clear, concise, and relevant explanations for a wide range of topics within the curriculum.

The primary goal is to offer an interactive learning experience where students can query the bot about specific DICT Module 3 concepts and receive well-formatted, easy-to-understand explanations, including practical code examples where applicable.

## Features

* **Intelligent Explanations:** Get detailed and context-aware explanations for DICT Module 3 topics, powered by Google Gemini 1.5 Flash.
* **Curriculum-Focused:** Responses are tailored to the KNEC DICT Module 3 syllabus, ensuring relevance.
* **Rich Formatting:** AI responses are rendered using Markdown, providing:
    * Clear headings for structured content.
    * Bold text for key terms and emphasis.
    * Bullet points and numbered lists for easy readability.
* **Code Highlighting:** Code examples provided by the AI are beautifully formatted with syntax highlighting, making them easy to read and understand.
* **User-Friendly Interface:** A simple web interface built with Flask allows for easy topic input and clear display of explanations.

## Technologies Used

* **Python 3:** The core programming language.
* **Flask:** A lightweight web framework for the backend.
* **Google Generative AI SDK (`google-generativeai`):** To interact with the Gemini API.
* **Python Markdown (`markdown`):** For converting Markdown-formatted AI responses into HTML.
* **Pygments:** Used by the Markdown library for robust syntax highlighting of code blocks.
* **`python-dotenv`:** For securely managing API keys and other environment variables during local development.
* **HTML/CSS:** For the frontend web interface.

## Setup Instructions (Local Development)

Follow these steps to get your AI Tutor Bot running on your local machine using VS Code.

### Prerequisites

* Python 3.x installed (recommended Python 3.8+)
* pip (Python package installer)
* Git (for cloning the repository)
* Visual Studio Code (or your preferred IDE)

### 🌐 Live Demo
* The KNEC DICT Module 3 Revision Bot is live and ready to use. It's deployed on Render, making it accessible to students anytime, anywhere.

👉 Try it out https://dict-module-3-revision-bot.onrender.com
(No login required — just enter a topic and get your explanation instantly.)
