from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import polars as pl

from .config import (
    MAJOR_SKILL_MAP_PATH,
    OCCUPATION_REFERENCE_PATH,
    PROCESSED_DIR,
)


@dataclass(frozen=True)
class RiskWeights:
    repetitive_task: float = 0.40
    ai_exposure: float = 0.30
    salary_stagnation: float = 0.20
    job_decline: float = 0.10


class CareerRiskModel:
    """Score career AI risk and recommend skill investments."""

    def __init__(
        self,
        occupation_reference_path: Path = OCCUPATION_REFERENCE_PATH,
        job_skills_path: Path = PROCESSED_DIR / "job_skills.csv",
        salary_history_path: Path = PROCESSED_DIR / "salary_history.csv",
        major_skill_map_path: Path = MAJOR_SKILL_MAP_PATH,
        weights: RiskWeights = RiskWeights(),
    ) -> None:
        self.occupation_reference_path = occupation_reference_path
        self.job_skills_path = job_skills_path
        self.salary_history_path = salary_history_path
        self.major_skill_map_path = major_skill_map_path
        self.weights = weights

    def occupation_scores(self) -> pl.DataFrame:
        occupations = pl.read_csv(self.occupation_reference_path)
        salary_history = pl.read_csv(self.salary_history_path)
        job_skills = pl.read_csv(self.job_skills_path)

        salary_growth = self._salary_growth(salary_history)
        demand = (
            job_skills.group_by("job_title")
            .agg(
                pl.len().alias("skill_mentions"),
                pl.n_unique("job_id").alias("posting_count"),
            )
            .rename({"job_title": "occupation"})
        )

        scored = (
            occupations.join(salary_growth, on="occupation", how="left")
            .join(demand, on="occupation", how="left")
            .with_columns(
                pl.col("salary_growth_pct").fill_null(0.0),
                pl.col("posting_count").fill_null(0),
                pl.col("skill_mentions").fill_null(0),
            )
            .with_columns(
                (100 - ((pl.col("salary_growth_pct") + 5).clip(0, 30) / 30 * 100))
                .round(2)
                .alias("salary_stagnation_score"),
                (100 - pl.col("future_outlook_score")).clip(0, 100).round(2).alias("job_decline_score_model"),
            )
            .with_columns(
                (
                    self.weights.repetitive_task * pl.col("repetitive_task_score")
                    + self.weights.ai_exposure * pl.col("ai_exposure_score")
                    + self.weights.salary_stagnation * pl.col("salary_stagnation_score")
                    + self.weights.job_decline * pl.col("job_decline_score_model")
                )
                .round(2)
                .alias("ai_risk_score")
            )
            .with_columns(
                (
                    0.55 * pl.col("future_outlook_score")
                    + 0.25 * (100 - pl.col("ai_risk_score"))
                    + 0.20 * (pl.col("posting_count") / pl.max("posting_count") * 100)
                )
                .round(2)
                .alias("future_demand_score")
            )
            .with_columns(
                pl.when(pl.col("ai_risk_score") >= 70)
                .then(pl.lit("High"))
                .when(pl.col("ai_risk_score") >= 45)
                .then(pl.lit("Medium"))
                .otherwise(pl.lit("Low"))
                .alias("risk_band")
            )
            .sort(["ai_risk_score", "future_demand_score"], descending=[True, False])
        )
        return scored

    def skill_value_ranking(self) -> pl.DataFrame:
        skill_metrics = pl.read_csv(PROCESSED_DIR / "skill_salary_metrics.csv")
        first_last = (
            skill_metrics.group_by("skill")
            .agg(
                pl.col("posting_year").min().alias("first_year"),
                pl.col("posting_year").max().alias("last_year"),
                pl.col("posting_count").sum().alias("posting_count"),
            )
            .join(
                skill_metrics.rename(
                    {"posting_year": "first_year", "avg_salary_usd": "first_salary_usd"}
                ).select("skill", "first_year", "first_salary_usd"),
                on=["skill", "first_year"],
                how="left",
            )
            .join(
                skill_metrics.rename({"posting_year": "last_year", "avg_salary_usd": "last_salary_usd"}).select(
                    "skill", "last_year", "last_salary_usd"
                ),
                on=["skill", "last_year"],
                how="left",
            )
            .with_columns(
                (
                    (pl.col("last_salary_usd") - pl.col("first_salary_usd"))
                    / pl.col("first_salary_usd")
                    * 100
                )
                .round(2)
                .alias("salary_growth_pct")
            )
            .filter(pl.col("posting_count") >= 5)
            .sort(["salary_growth_pct", "last_salary_usd"], descending=True)
        )
        return first_last

    def simulate_student(self, major: str, skills: list[str], top_n: int = 5) -> pl.DataFrame:
        scores = self.occupation_scores()
        job_skills = pl.read_csv(self.job_skills_path)
        major_map = pl.read_csv(self.major_skill_map_path)

        normalized_skills = {skill.strip().lower() for skill in skills if skill.strip()}
        major_skills = (
            major_map.filter(pl.col("major").str.to_lowercase() == major.strip().lower())
            .select("recommended_base_skills")
            .to_series()
            .to_list()
        )
        for item in major_skills:
            normalized_skills.update(skill.strip().lower() for skill in item.split("|"))

        occupation_skill_stats = (
            job_skills.group_by("job_title", "skill")
            .agg(pl.len().alias("mentions"), pl.mean("salary_usd").alias("skill_salary"))
            .rename({"job_title": "occupation"})
        )

        records = []
        for occupation in scores["occupation"].to_list():
            occupation_skills = (
                occupation_skill_stats.filter(pl.col("occupation") == occupation)
                .sort(["mentions", "skill_salary"], descending=True)
                .select("skill")
                .to_series()
                .to_list()
            )
            required = occupation_skills[:8]
            matched = [skill for skill in required if skill in normalized_skills]
            gaps = [skill for skill in required if skill not in normalized_skills][:4]
            match_score = round(len(matched) / max(len(required), 1) * 100, 2)
            records.append(
                {
                    "occupation": occupation,
                    "skill_match_score": match_score,
                    "matched_skills": "|".join(matched),
                    "recommended_skills": "|".join(gaps),
                }
            )

        fit = pl.DataFrame(records)
        return (
            scores.join(fit, on="occupation", how="left")
            .with_columns(
                (
                    0.45 * pl.col("future_demand_score")
                    + 0.35 * pl.col("skill_match_score")
                    + 0.20 * (100 - pl.col("ai_risk_score"))
                )
                .round(2)
                .alias("student_fit_score")
            )
            .sort("student_fit_score", descending=True)
            .head(top_n)
        )

    @staticmethod
    def _salary_growth(salary_history: pl.DataFrame) -> pl.DataFrame:
        bounds = salary_history.group_by("job_title").agg(
            pl.col("posting_year").min().alias("first_year"),
            pl.col("posting_year").max().alias("last_year"),
        )
        first = salary_history.rename(
            {"job_title": "occupation", "posting_year": "first_year", "avg_salary_usd": "first_salary_usd"}
        ).select("occupation", "first_year", "first_salary_usd")
        last = salary_history.rename(
            {"job_title": "occupation", "posting_year": "last_year", "avg_salary_usd": "last_salary_usd"}
        ).select("occupation", "last_year", "last_salary_usd")
        return (
            bounds.rename({"job_title": "occupation"})
            .join(first, on=["occupation", "first_year"], how="left")
            .join(last, on=["occupation", "last_year"], how="left")
            .with_columns(
                (
                    (pl.col("last_salary_usd") - pl.col("first_salary_usd"))
                    / pl.col("first_salary_usd")
                    * 100
                )
                .round(2)
                .alias("salary_growth_pct")
            )
            .select("occupation", "first_year", "last_year", "first_salary_usd", "last_salary_usd", "salary_growth_pct")
        )

