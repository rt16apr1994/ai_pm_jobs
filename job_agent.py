import os
import requests
from ddgs import DDGS
from google import genai  # <--- New import style

# Initialize the new Client
# It automatically looks for GEMINI_API_KEY in your environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def search_jobs():
    query = 'AI Product Manager remote India'
    with DDGS() as ddgs:
        return ddgs.text(query, max_results=10)

def filter_with_ai(job_list):
    prompt = f"""
    Filter the following job list for "AI Product Manager" roles that are Remote and based in India.
    Results: {job_list}
    If no matches, respond with "NO_MATCH".
    """
    
    # New method signature: client.models.generate_content
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    return response.text

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    raw_jobs = search_jobs()
    if raw_jobs:
        ai_analysis = filter_with_ai(raw_jobs)
        if "NO_MATCH" not in ai_analysis:
            send_telegram("*🚀 Agentic Filtered Jobs:*\n\n" + ai_analysis)
