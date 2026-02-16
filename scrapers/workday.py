import requests

def fetch_workday_jobs(base_url):
    api_url = f"{base_url}/jobs"
    response = requests.get(api_url)
    data = response.json()

    jobs = []

    for job in data.get("jobPostings", []):
        jobs.append({
            "id": job.get("bulletFields", [""])[0] + job.get("title", ""),
            "title": job.get("title", ""),
            "location": job.get("locationsText", ""),
            "posted": job.get("postedOn", ""),
            "url": base_url + job.get("externalPath", "")
        })

    return jobs
