# Note-Taking Assistant

Welcome to the Note-Taking Assistant repository! This project provides a sophisticated note-taking application powered by advanced language models and web search tools. It allows users to manage, expand, and enhance their notes using AI-driven insights.

## Medium Article

For a detailed walkthrough of how this application was built, check out my Medium article: [Building a Smart Note-Taking Assistant with LangChain and Groq](https://medium.com/@insatiablerohit/building-a-smart-note-taking-assistant-with-langchain-and-groq-part-0-laying-the-foundation-dde4297e07d4).


## Features

- **Note Management**: Save and manage your notes locally.
- **Question Answering**: Ask questions related to your notes and receive AI-generated responses.
- **Web Search Integration**: Retrieve and incorporate relevant web search results to enrich your notes.
- **Dynamic Workflow**: Uses a state graph to intelligently route questions between note-based responses and web searches.

## Getting Started

To get started with the Note-Taking Assistant, follow these steps:

### Prerequisites

- Python 3.7 or higher
- Flask
- LangChain
- Groq API
- DuckDuckGo API

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/note-taking-assistant.git
    cd note-taking-assistant
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment variables:**

    Create a `.env` file in the root directory of the project with the following content:

    ```
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_API_KEY=your_langchain_api_key
    LANGCHAIN_PROJECT=L3 Note-taking Assistant
    GROQ_API_KEY=your_groq_api_key
    ```

    Replace `your_langchain_api_key` and `your_groq_api_key` with your actual API keys.

### Running the Application

1. **Start the Flask server:**

    ```bash
    python app.py
    ```

2. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:5000` to access the application interface.

### Usage

- **Saving Notes**: Write notes in the designated text area and click "Save Notes" to store them locally.
- **Asking Questions**: Enter your question in the provided input field, and the AI will generate a response based on your notes and web search results.
- **View Responses**: Responses will be displayed in the designated area of the web interface.

### API Endpoints

- **`POST /api/save_notes`**: Save notes to a file. 
  - **Request Body**: JSON with a `notes` field containing the notes text.
  - **Response**: JSON indicating the status of the save operation.

- **`POST /api/ask`**: Ask a question related to your notes.
  - **Request Body**: JSON with `question` and `context` fields.
  - **Response**: JSON with the AI-generated response to the question.

### Configuration

- **`app.py`**: The main application file. You can modify the prompts, API keys, and other settings here.
- **`static/index.html`**: The HTML file for the application’s front-end. Customize the interface as needed.
- **`static/styles.css`**: The CSS file for styling the application. Update the styles to match your preferences.

### Contributing

Contributions are welcome! If you have suggestions or improvements, please submit a pull request or open an issue.


