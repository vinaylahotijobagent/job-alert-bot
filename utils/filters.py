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

LOCATION = "Hyderabad"

def keyword_match(title):
    title = title.lower()
    return any(k in title for k in KEYWORDS)

def location_match(location):
    return LOCATION.lower() in location.lower()
