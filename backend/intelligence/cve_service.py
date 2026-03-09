import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

NVD_API_KEY = os.getenv("NVD_API_KEY")


def fetch_cve_data(keyword):
    """
    Fetch CVE data from NVD based on keyword.
    Returns CVSS score and CVE ID if found.
    """

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    headers = {
        "apiKey": NVD_API_KEY
    }

    params = {
        "keywordSearch": keyword,
        "resultsPerPage": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        vulnerabilities = data.get("vulnerabilities", [])

        if not vulnerabilities:
            return None

        cve = vulnerabilities[0]["cve"]
        cve_id = cve["id"]

        metrics = cve.get("metrics", {})
        cvss_score = None

        if "cvssMetricV31" in metrics:
            cvss_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]

        return {
            "cve_id": cve_id,
            "cvss_score": cvss_score
        }

    except Exception as e:
        print("CVE lookup failed:", e)
        return None
