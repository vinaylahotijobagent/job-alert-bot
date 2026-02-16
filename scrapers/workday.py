import requests

def fetch_workday_jobs(company_config):

    host = company_config["host"]
    tenant = company_config["tenant"]
    career_site = company_config["career_site"]

    url = f"https://{host}/wday/cxs/{tenant}/{career_site}/jobs"

    payload = {
        "appliedFacets": {},
        "limit": 50,
        "offset": 0,
        "searchText": ""
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": f"https://{host}",
        "Referer": f"https://{host}/recruiting/{tenant}/{career_site}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Response preview:", response.text[:300])
        return []

    data = response.json()

    jobs = []

    for job in data.get("jobPostings", []):
        jobs.append({
            "id": job.get("externalPath", ""),
            "title": job.get("title", ""),
            "location": job.get("locationsText", ""),
            "posted": job.get("postedOn", ""),
            "url": f"https://{host}{job.get('externalPath', '')}"
        })

    print("Jobs fetched:", len(jobs))

    return jobs
