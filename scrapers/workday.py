import requests

def fetch_workday_jobs(company_config):
    """
    Universal Workday V2 scraper.
    Works for modern Workday career sites.
    """

    host = company_config["host"]
    tenant = company_config["tenant"]
    career_site = company_config["career_site"]

    url = f"https://{host}/wday/cxs/{tenant}/{career_site}/jobs"

    payload = {
        "limit": 50,
        "offset": 0,
        "searchText": ""
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": f"https://{host}",
        "Referer": f"https://{host}/"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
    except Exception as e:
        print(f"Request failed for {company_config['company']}: {e}")
        return []

    print(f"{company_config['company']} status: {response.status_code}")

    if response.status_code != 200:
        print("Response preview:", response.text[:300])
        return []

    try:
        data = response.json()
    except Exception:
        print("Response was not JSON")
        print(response.text[:300])
        return []

    jobs = []

    for job in data.get("jobPostings", []):
        jobs.append({
            "id": f"{job.get('title','')}-{job.get('locationsText','')}",
            "title": job.get("title", ""),
            "location": job.get("locationsText", ""),
            "posted": job.get("postedOn", ""),
            "url": f"https://{host}{job.get('externalPath', '')}"
        })

    print(f"{company_config['company']} jobs fetched:", len(jobs))

    return jobs
