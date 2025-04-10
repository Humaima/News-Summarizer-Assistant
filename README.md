# News Summarizer Assistant 📰

An AI-powered news summarization tool that fetches and summarizes the latest articles based on user queries.
![image](https://github.com/user-attachments/assets/4522caee-91bf-43bb-a8c7-5eee49b70742)

## Features

- Custom news search with filters
- AI-generated summaries (using Groq/llama 3.3 70b versatile)
- Related article suggestions
- Multi-language support
- Responsive web interface
![image](https://github.com/user-attachments/assets/3bdc1ee9-f17d-4a85-a563-4361cbe9aa4b)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news-summarizer-assistant.git
   cd news-summarizer-assistant
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
4. Create .env file:
   ```bash
   cp .env.example .env
   Add your API keys to .env
5. Run the app:
   ```bash
   streamlit run app.py
   
## Configurations
Get API keys:
- GNews API
- Groq API

## Tech Stack
- Python 3.8+
- Streamlit (UI)
- Groq API (LLM)
- GNews API (News)
- FAISS (Vector DB)
- Sentence Transformers (Embeddings)

