import os
import requests
from ddgs import DDGS
from google import genai  # <--- New import style

# Initialize the new Client
# It automatically looks for GEMINI_API_KEY in your environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def search_jobs():
    query = 'site:linkedin.com/jobs "AI Product Manager" remote India "posted 1 week ago"'
    with DDGS() as ddgs:
        return ddgs.text(query, max_results=10)

def filter_with_ai(job_list):
    # We add a specific instruction to the prompt to avoid JSON formatting
    prompt = f"""
    You are a career assistant. Review these jobs: {job_list}
    
    Filter for "AI Product Manager" roles in India/Remote.
    Return a bulleted list with the Title and a clickable Markdown Link.
    
    Example format:
    * [Job Title](URL) - Brief reason why it matches.
    
    If no matches found, respond ONLY with the word: NO_MATCH
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    # Use .text to get the string content
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
        
        # Strip whitespace to ensure "NO_MATCH" check works
        clean_analysis = ai_analysis.strip()
        
        if "NO_MATCH" not in clean_analysis:
            # We send the text directly now
            send_telegram(f"🤖 *AI Agent Recommendations:*\n\n{clean_analysis}")
        else:
            print("AI decided none of the results were a high-quality match.")
