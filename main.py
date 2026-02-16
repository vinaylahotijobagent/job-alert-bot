import os
import json
import requests
from serpapi import GoogleSearch
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
SERPAPI_KEY = os.environ["SERPAPI_KEY"]

LOCATION = "Hyderabad"
POSTED_WITHIN_HOURS = 24

KEYWORDS = [
    "data analyst",
    "business intelligence",
    "bi",
    "power bi",
    "tableau",
    "databricks",
    "azure",
    "python",
    "analytics",
    "data engineer"
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def load_json(file):
    if os.path.exists(file):
        with open(file) as f:
            return json.load(f)
    return []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

def is_recent(posted_at):
    if not posted_at:
        return False
    posted_at = posted_at.lower()
    if "hour" in posted_at:
        return True
    if "1 day" in posted_at:
        return True
    return False

def keyword_match(title):
    title = title.lower()
    return any(keyword in title for keyword in KEYWORDS)

def search_jobs(company):
    params = {
        "engine": "google_jobs",
        "q": f"{company} jobs in {LOCATION}",
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("jobs_results", [])

def main():
    companies = load_json("companies.json")
    seen_jobs = load_json("seen_jobs.json")
    new_seen = seen_jobs.copy()

    alerts = []

    for company in companies:
        print(f"Checking {company}...")
        jobs = search_jobs(company)

        for job in jobs:
            job_id = job.get("job_id")
            if not job_id or job_id in seen_jobs:
                continue

            title = job.get("title", "")
            location = job.get("location", "")
            posted = job.get("detected_extensions", {}).get("posted_at", "")
            link = job.get("apply_options", [{}])[0].get("link", "")

            if LOCATION.lower() not in location.lower():
                continue

            if not is_recent(posted):
                continue

            if not keyword_match(title):
                continue

            alert_text = (
                f"<b>{title}</b>\n"
                f"{company}\n"
                f"{location}\n"
                f"{posted}\n"
                f"{link}\n\n"
            )

            alerts.append(alert_text)
            new_seen.append(job_id)

    if alerts:
        message = "🚀 <b>New Data/BI Jobs - Hyderabad (Last 24h)</b>\n\n"
        message += "".join(alerts[:10])
        send_telegram_message(message)
        print("Alert sent.")
    else:
        print("No new jobs.")

    save_json("seen_jobs.json", new_seen)

if __name__ == "__main__":
    main()
