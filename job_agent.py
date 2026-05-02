import os
import requests
from ddgs import DDGS
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def search_jobs():
    query = 'site:linkedin.com/jobs "AI Product Manager" remote India "posted 1 week ago"'
    with DDGS() as ddgs:
        return ddgs.text(query, max_results=10)

def filter_with_ai(job_list):
    # This is the "Agentic" prompt
    prompt = f"""
    I am looking for "AI Product Manager" jobs that are Remote and based in or hiring from India.
    Below is a list of raw search results. 
    
    Filter this list and return ONLY the jobs that are a 90% match for an AI Product Manager role.
    For each matching job, provide the title and the link.
    
    Search Results:
    {job_list}
    
    If no jobs match, simply say "NO_MATCH".
    """
    response = model.generate_content(prompt)
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
        # The Agent "thinks" here
        ai_analysis = filter_with_ai(raw_jobs)
        
        if "NO_MATCH" not in ai_analysis:
            header = "*🤖 AI Agent Analysis: Top Matches Found*\n\n"
            send_telegram(header + ai_analysis)
        else:
            print("AI found no relevant matches today.")
