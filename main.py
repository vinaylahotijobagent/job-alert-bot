import json
from scrapers.workday import fetch_workday_jobs
from scrapers.oracle import fetch_oracle_jobs
from notifier.telegram import send_message
from utils.filters import keyword_match, location_match
from utils.storage import load_seen, save_seen


def load_config():
    with open("config.json") as f:
        return json.load(f)


def main():
    config = load_config()
    seen = load_seen()
    new_seen = seen.copy()
    alerts = []

    for company in config:

        if company["ats"] == "workday":
            jobs = fetch_workday_jobs(company)

        elif company["ats"] == "oracle":
            jobs = fetch_oracle_jobs(company)

        else:
            continue

        for job in jobs:

            if job["id"] in seen:
                continue

            if not keyword_match(job["title"]):
                continue

            if not location_match(job["location"]):
                continue

            alert = (
                f"<b>{job['title']}</b>\n"
                f"{company['company']}\n"
                f"{job['location']}\n"
                f"{job['url']}\n\n"
            )

            alerts.append(alert)
            new_seen.append(job["id"])

    if alerts:
        message = "🚀 <b>New Data/BI Jobs - Hyderabad</b>\n\n"
        message += "".join(alerts[:10])
        send_message(message)

    save_seen(new_seen)


if __name__ == "__main__":
    main()
