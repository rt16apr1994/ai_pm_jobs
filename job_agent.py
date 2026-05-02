import os
import requests
from duckduckgo_search import DDGS

def search_jobs():
    # A more flexible query to ensure results
    query = '"AI Product Manager" remote India'
    results = []
    
    with DDGS() as ddgs:
        # Looking for recent results
        resp = ddgs.text(query, max_results=10)
        for r in resp:
            results.append(r)
    return results

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    jobs = search_jobs()
    
    if jobs:
        header = "*🚀 AI Product Manager Jobs (India/Remote)*\n\n"
        job_list = []
        for j in jobs:
            job_list.append(f"🔹 [{j['title']}]({j['href']})")
        
        full_message = header + "\n\n".join(job_list)
        send_telegram(full_message)
    else:
        # Send a confirmation even if no jobs are found so you know it ran
        send_telegram("✅ Job search completed, but no new listings were found for today.")
