import json
import sqlite3
from datetime import datetime, timezone

from joblens.config import DB_PATH
from joblens.mappers import map_job_ninja, map_job_remotive, ninja_key, remotive_key

SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_jobs (
    source TEXT NOT NULL,
    source_job_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    UNIQUE (source, source_job_id)
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_job_id TEXT NOT NULL,
    url TEXT,
    title TEXT,
    company_name TEXT,
    category TEXT,
    tags TEXT,
    job_type TEXT,
    salary TEXT,
    description TEXT,
    company_logo_url TEXT,
    location TEXT,
    published_at TEXT,
    UNIQUE (source, source_job_id)
);
"""


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db(conn):
    with conn:
        conn.executescript(SCHEMA)


def insert_raw(jobs_remotive, jobs_ninja, conn):
    sql_raw = """
    INSERT INTO raw_jobs (source, source_job_id, payload, fetched_at)
    VALUES (?, ?, ?, ?)
    ON CONFLICT (source, source_job_id) DO UPDATE SET
        payload = excluded.payload,
        fetched_at = excluded.fetched_at
    """
    fetched_at = datetime.now(timezone.utc).isoformat()
    sources = [
        ("remotive", remotive_key, jobs_remotive),
        ("openwebninja", ninja_key, jobs_ninja),
    ]
    with conn:
        for source, key_func, jobs in sources:
            for job in jobs:
                conn.execute(
                    sql_raw,
                    (source, key_func(job), json.dumps(job), fetched_at),
                )


def insert_jobs(jobs_remotive, jobs_ninja, conn):
    sql_jobs = """
    INSERT INTO jobs
    (source, source_job_id, url, title, company_name, category, tags, job_type,
    salary, description, company_logo_url, location, published_at)
    VALUES
    (:source, :source_job_id, :url, :title, :company_name, :category, :tags, :job_type,
    :salary, :description, :company_logo_url, :location, :published_at)
    ON CONFLICT (source, source_job_id) DO UPDATE SET
        url = excluded.url,
        title = excluded.title,
        company_name = excluded.company_name,
        category = excluded.category,
        tags = excluded.tags,
        job_type = excluded.job_type,
        salary = excluded.salary,
        description = excluded.description,
        company_logo_url = excluded.company_logo_url,
        location = excluded.location,
        published_at = excluded.published_at
    """
    mappers = [(map_job_remotive, jobs_remotive), (map_job_ninja, jobs_ninja)]
    with conn:
        for mapper, jobs in mappers:
            for job in jobs:
                conn.execute(sql_jobs, mapper(job))
