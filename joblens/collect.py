import requests

from joblens.config import NINJA_API_KEY, NINJA_QUERIES, NINJA_URL, REMOTIVE_URL
from joblens.db import get_connection, init_db, insert_jobs, insert_raw


def fetch_remotive():
    try:
        response = requests.get(REMOTIVE_URL, timeout=10)
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        return []

    if response.status_code == 200:
        return response.json()["jobs"]

    print(f"Failed to fetch Remotive jobs. Status code: {response.status_code}")
    return []


def fetch_ninja_query(query):
    headers = {"X-API-Key": NINJA_API_KEY}
    try:
        response = requests.get(
            NINJA_URL,
            headers=headers,
            params={"query": query},
            timeout=10,
        )
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        return []

    if response.status_code == 200:
        return response.json()["data"]["jobs"]

    print(f"Failed to fetch OpenWebNinja jobs. Status code: {response.status_code}")
    return []


def fetch_ninja():
    jobs = []
    for query in NINJA_QUERIES:
        jobs.extend(fetch_ninja_query(query))
    return jobs


def main():
    conn = get_connection()
    try:
        init_db(conn)
        jobs_remotive = fetch_remotive()
        jobs_ninja = fetch_ninja()
        insert_raw(jobs_remotive, jobs_ninja, conn)
        insert_jobs(jobs_remotive, jobs_ninja, conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()