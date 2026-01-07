# Pangea Digital Twin Moderator

A robust AI moderation system designed to safeguard Large Language Model (LLM) interactions. This project implements a comprehensive pipeline that filters malicious inputs and ensures safe outputs by leveraging multiple AI models and a "Generate & Select" strategy.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## 🚀 Features

-   **🛡️ Multi-Stage Pipeline**:
    -   **Input Moderation (Groq)**: Analyzes user prompts for injection attacks, hate speech, and other violations using a configurable system prompt.
    -   **Diverse Generation (Local LLM)**: Generates 10 distinct responses with varying tones (formal, sarcastic, etc.) using `llama3.1:8b` via Ollama.
    -   **Output Filtering (Mistral)**: Evaluates the safety of all generated responses and selects the 2 safest ones for display.

-   **💻 Modern Web Interface**:
    -   Sleek, dark-themed UI with glassmorphism design.
    -   Real-time chat interface displaying the two safest answers.
    -   Visual pipeline status indicators.

-   **⚙️ Dynamic Configuration**:
    -   **Settings Tab**: Integrated UI to view and modify the Groq system prompt (Discriminator Policy) in real-time.
    -   **Database Persistence**: Custom system prompts are stored in SQLite, allowing persistent configuration changes.
    -   **Reset Capability**: One-click restore to the default safety policy.

-   **📊 Logging & Auditing**:
    -   Logs accepted and rejected prompts for analysis.
    -   detailed rationale for rejected prompts.

## 🛠️ Architecture

1.  **User Input** -> **Groq API**:
    -   Checks for Prompt Injection/Jailbreaks.
    -   *If Violation*: Request is blocked immediately with a rationale.
    -   *If Safe*: Proceed to generation.
2.  **Generator (Ollama - Llama 3.1)**:
    -   Produces 10 parallel responses with different personas/tones.
3.  **Moderator (Ollama - Mistral)**:
    -   Scores each response for safety.
4.  **Selection**:
    -   The system picks the 2 responses with the lowest risk scores.
5.  **UI Display**:
    -   The safe responses are presented to the user.

## 📋 Prerequisites

-   **Python 3.8+**
-   **Ollama**: Must be installed and running locally.
-   **Groq API Key**: For the input moderation layer.

### Required AI Models
Ensure you have pulled the necessary models in Ollama:
```bash
ollama pull llama3.1:8b
ollama pull mistral
```

## ⚙️ Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/Pangea-digital-twin-moderator.git
    cd Pangea-digital-twin-moderator/moderator
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the `moderator` directory (same level as `manage.py`) and add your Groq API key:
    ```env
    GROQ_API_KEY=gsk_your_key_here
    ```

5.  **Initialize Database**
    Run the migrations to set up the SQLite database (including the new Settings feature tables):
    ```bash
    python manage.py makemigrations chat_moderator
    python manage.py migrate
    ```

## 🚀 Usage

1.  **Start the Ollama Server** (if not already running)
    ```bash
    ollama serve
    ```

2.  **Run the Django Server**
    ```bash
    python manage.py runserver
    ```

3.  **Access the Application**
    Open your browser and navigate to: `http://127.0.0.1:8000/`

4.  **Using the Settings Tab**
    -   Click the **⚙️ Paramètres** tab in the top navigation.
    -   View the current System Prompt used by Groq.
    -   Edit the prompt to customize safety rules or injection detection logic.
    -   Click **Enregistrer** to save changes.
    -   Click **Réinitialiser** to revert to the default robust policy.

## 📁 Project Structure

```
moderator/
├── chat_moderator/       # Django app for views and models
│   ├── models.py         # DB models (SystemPromptConfig, etc.)
│   ├── views.py          # API endpoints and view logic
│   └── urls.py           # URL routing
├── db/                   # Database logic
│   ├── database.py       # Functions to save prompts
│   └── db.sqlite3        # SQLite database file
├── src/                  # Core AI Logic
│   ├── run_groq.py       # Groq moderation implementation
│   ├── query.py          # Main pipeline (Ollama + moderations)
│   └── discriminator.py  # Mistral moderation logic
├── templates/
│   └── ui.html           # Main frontend interface
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
