from __future__ import annotations

from pathlib import Path

import duckdb

from .config import OCCUPATION_REFERENCE_PATH, PROCESSED_DIR, WAREHOUSE_DIR, WAREHOUSE_PATH


def build_warehouse(
    processed_dir: Path = PROCESSED_DIR,
    occupation_reference_path: Path = OCCUPATION_REFERENCE_PATH,
    warehouse_path: Path = WAREHOUSE_PATH,
) -> Path:
    """Build a DuckDB warehouse from processed CSV tables."""
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(warehouse_path))
    try:
        con.execute("DROP TABLE IF EXISTS jobs")
        con.execute("DROP TABLE IF EXISTS skills")
        con.execute("DROP TABLE IF EXISTS salary_history")
        con.execute("DROP TABLE IF EXISTS occupation")

        con.execute(
            """
            CREATE TABLE jobs AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(processed_dir / "jobs_clean.csv")],
        )
        con.execute(
            """
            CREATE TABLE skills AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(processed_dir / "job_skills.csv")],
        )
        con.execute(
            """
            CREATE TABLE salary_history AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(processed_dir / "salary_history.csv")],
        )
        con.execute(
            """
            CREATE TABLE occupation AS
            SELECT *
            FROM read_csv_auto(?)
            """,
            [str(occupation_reference_path)],
        )
        con.execute("CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(job_title)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_skills_skill ON skills(skill)")
    finally:
        con.close()
    return warehouse_path


def run_analysis_query(sql: str, warehouse_path: Path = WAREHOUSE_PATH):
    con = duckdb.connect(str(warehouse_path), read_only=True)
    try:
        return con.execute(sql).fetchdf()
    finally:
        con.close()


if __name__ == "__main__":
    print(build_warehouse())

