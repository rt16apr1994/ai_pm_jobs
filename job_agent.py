import os
import requests
from duckduckgo_search import DDGS

def search_jobs():
    query = 'site:linkedin.com/jobs/ OR site:indeed.com "AI Product manager" remote India "posted 1 week ago"'
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
    return results

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    jobs = search_jobs()
    if jobs:
        msg = "*Today's Job Leads:*\n\n" + "\n\n".join([f"[{j['title']}]({j['href']})" for j in jobs])
        send_telegram(msg)
