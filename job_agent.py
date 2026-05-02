import os
import requests
from ddgs import DDGS

def search_jobs():
    # Broader query to ensure we find SOMETHING for testing
    query = 'AI Product Manager remote India'
    print(f"Searching for: {query}")
    
    with DDGS() as ddgs:
        # Latest 2026 'text' method returns a list of dicts directly
        results = ddgs.text(query, max_results=5)
    
    print(f"Found {len(results)} jobs.")
    return results

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Error: Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in GitHub Secrets.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    print(f"Telegram Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    job_results = search_jobs()
    
    if job_results:
        msg = "*🚀 Today's AI PM Jobs*\n\n"
        for job in job_results:
            msg += f"🔹 [{job['title']}]({job['href']})\n"
        send_telegram(msg)
    else:
        send_telegram("🔍 Search completed, but no jobs were found today.")
