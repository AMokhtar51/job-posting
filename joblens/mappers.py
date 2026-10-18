import json

from bs4 import BeautifulSoup


def remotive_key(job):
    return str(job["id"])


def ninja_key(job):
    return job["job_apply_link"]


def clean_job_description(raw_description=""):
    raw_description = raw_description or ""
    html_tree = BeautifulSoup(raw_description, "lxml")
    description = html_tree.get_text()
    description = description.splitlines()
    description = [line.strip() for line in description if line.strip()]
    return "\n".join(description)


def map_job_remotive(job):
    return {
        "source": "remotive",
        "source_job_id": remotive_key(job),
        "url": job["url"],
        "title": job["title"],
        "company_name": job["company_name"],
        "category": job["category"],
        "tags": json.dumps(job["tags"]),
        "job_type": job["job_type"],
        "salary": job["salary"] or None,
        "description": clean_job_description(job["description"]),
        "company_logo_url": job["company_logo_url"],
        "location": job["candidate_required_location"],
        "published_at": job["publication_date"],
    }


def map_job_ninja(job):
    return {
        "source": "openwebninja",
        "source_job_id": ninja_key(job),
        "url": job["job_apply_link"],
        "title": job["job_title"],
        "company_name": job["employer_name"],
        "category": None,
        "tags": None,
        "job_type": job["job_employment_type"],
        "salary": job["job_salary"] or None,
        "description": clean_job_description(job["job_description"]),
        "company_logo_url": job["employer_logo"],
        "location": job["job_location"],
        "published_at": job["job_posted_at_datetime_utc"],
    }
