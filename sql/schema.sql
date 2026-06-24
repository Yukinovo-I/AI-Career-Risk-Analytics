-- DuckDB-compatible warehouse schema for AI Career Risk Analytics.

CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR PRIMARY KEY,
    job_title VARCHAR NOT NULL,
    company VARCHAR,
    location VARCHAR,
    country VARCHAR,
    salary_usd DOUBLE,
    salary_log DOUBLE,
    skills_norm VARCHAR,
    experience_level VARCHAR,
    posting_date DATE,
    posting_year INTEGER,
    source VARCHAR
);

CREATE TABLE IF NOT EXISTS skills (
    job_id VARCHAR,
    job_title VARCHAR,
    posting_year INTEGER,
    salary_usd DOUBLE,
    skill VARCHAR,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE IF NOT EXISTS salary_history (
    job_title VARCHAR,
    posting_year INTEGER,
    avg_salary_usd DOUBLE,
    median_salary_usd DOUBLE,
    posting_count INTEGER
);

CREATE TABLE IF NOT EXISTS occupation (
    occupation VARCHAR PRIMARY KEY,
    soc_code VARCHAR,
    occupation_family VARCHAR,
    repetitive_task_score DOUBLE,
    ai_exposure_score DOUBLE,
    future_outlook_score DOUBLE,
    job_decline_reference_score DOUBLE,
    demand_growth_pct DOUBLE,
    source_note VARCHAR
);

