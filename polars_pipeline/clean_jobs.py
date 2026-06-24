from __future__ import annotations

from pathlib import Path

import polars as pl

from .config import PROCESSED_DIR, RAW_JOBS_PATH


def clean_jobs(raw_path: Path = RAW_JOBS_PATH, output_dir: Path = PROCESSED_DIR) -> dict[str, Path]:
    """Clean raw job postings and create normalized job and skill tables."""
    output_dir.mkdir(parents=True, exist_ok=True)

    jobs = (
        pl.scan_csv(raw_path)
        .filter(pl.col("salary").is_not_null())
        .with_columns(
            pl.col("job_title").str.strip_chars().alias("job_title"),
            pl.col("company").str.strip_chars().alias("company"),
            pl.col("location").str.strip_chars().alias("location"),
            pl.col("country").str.strip_chars().alias("country"),
            pl.col("skills").str.to_lowercase().str.replace_all(r"\s*\|\s*", "|").alias("skills_norm"),
            pl.col("experience").str.to_lowercase().str.strip_chars().alias("experience_level"),
            pl.col("salary").cast(pl.Float64).alias("salary_usd"),
            pl.col("date_posted").str.to_date("%Y-%m-%d").alias("posting_date"),
        )
        .with_columns(
            pl.col("posting_date").dt.year().alias("posting_year"),
            pl.col("salary_usd").log().alias("salary_log"),
        )
        .select(
            "job_id",
            "job_title",
            "company",
            "location",
            "country",
            "salary_usd",
            "salary_log",
            "skills_norm",
            "experience_level",
            "posting_date",
            "posting_year",
            "source",
        )
    )

    jobs_df = jobs.collect()
    jobs_path = output_dir / "jobs_clean.csv"
    jobs_df.write_csv(jobs_path)

    job_skills_df = (
        jobs_df.lazy()
        .select("job_id", "job_title", "posting_year", "salary_usd", "skills_norm")
        .with_columns(pl.col("skills_norm").str.split("|").alias("skill"))
        .explode("skill")
        .with_columns(pl.col("skill").str.strip_chars().alias("skill"))
        .filter(pl.col("skill") != "")
        .select("job_id", "job_title", "posting_year", "salary_usd", "skill")
        .collect()
    )
    job_skills_path = output_dir / "job_skills.csv"
    job_skills_df.write_csv(job_skills_path)

    salary_history_df = (
        jobs_df.lazy()
        .group_by("job_title", "posting_year")
        .agg(
            pl.mean("salary_usd").round(2).alias("avg_salary_usd"),
            pl.median("salary_usd").round(2).alias("median_salary_usd"),
            pl.len().alias("posting_count"),
        )
        .sort(["job_title", "posting_year"])
        .collect()
    )
    salary_history_path = output_dir / "salary_history.csv"
    salary_history_df.write_csv(salary_history_path)

    skill_metrics_df = (
        job_skills_df.lazy()
        .group_by("skill", "posting_year")
        .agg(
            pl.mean("salary_usd").round(2).alias("avg_salary_usd"),
            pl.len().alias("posting_count"),
        )
        .sort(["skill", "posting_year"])
        .collect()
    )
    skill_metrics_path = output_dir / "skill_salary_metrics.csv"
    skill_metrics_df.write_csv(skill_metrics_path)

    return {
        "jobs": jobs_path,
        "job_skills": job_skills_path,
        "salary_history": salary_history_path,
        "skill_metrics": skill_metrics_path,
    }


if __name__ == "__main__":
    outputs = clean_jobs()
    for name, path in outputs.items():
        print(f"{name}: {path}")

