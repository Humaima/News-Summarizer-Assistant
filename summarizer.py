from groq import Groq
from config import Config
import time

class NewsSummarizer:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        
    def summarize(self, text, max_length=150):
        try:
            prompt = (
                f"Please provide a concise 2-3 sentence summary of the following news content. "
                f"Focus on the key facts and main points. Write in clear, simple language.\n\n"
                f"Content to summarize:\n{text}\n\n"
                f"Summary:"
            )
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a news summarization assistant. Provide accurate, neutral summaries of news content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=Config.MODEL_NAME,
                max_tokens=max_length,
                temperature=0.5, 
                top_p=0.9,
            )
            
            summary = response.choices[0].message.content.strip()
            # Clean up any odd formatting
            summary = summary.replace('"', '').replace('\n', ' ')
            return summary
            
        except Exception as e:
            print(f"Summarization error: {str(e)}")
            time.sleep(2)  # Rate limiting
            return "Summary unavailable at this time."