import requests

def fetch_oracle_jobs(base_url):
    params = {
        "q": "",
        "limit": 50,
        "offset": 0
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    jobs = []

    for job in data.get("items", []):
        jobs.append({
            "id": job.get("Id"),
            "title": job.get("Title"),
            "location": job.get("PrimaryLocation"),
            "posted": job.get("PostedDate"),
            "url": job.get("ExternalApplyURL")
        })

    return jobs
