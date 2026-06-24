from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from polars_pipeline.clean_jobs import clean_jobs
from polars_pipeline.risk_model import CareerRiskModel


ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_outputs_have_expected_tables() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_sample_data.py")], check=True)
    outputs = clean_jobs()
    assert {"jobs", "job_skills", "salary_history", "skill_metrics"} == set(outputs)
    assert outputs["jobs"].exists()
    assert outputs["job_skills"].exists()


def test_risk_scores_are_bounded_and_rank_high_repetitive_roles() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_sample_data.py")], check=True)
    clean_jobs()
    scores = CareerRiskModel().occupation_scores()
    assert scores["ai_risk_score"].min() >= 0
    assert scores["ai_risk_score"].max() <= 100

    data_entry = scores.filter(scores["occupation"] == "Data Entry Clerk")["ai_risk_score"][0]
    ml_engineer = scores.filter(scores["occupation"] == "Machine Learning Engineer")["ai_risk_score"][0]
    assert data_entry > ml_engineer


def test_student_simulator_recommends_skills() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_sample_data.py")], check=True)
    clean_jobs()
    result = CareerRiskModel().simulate_student("Mathematics", ["SQL", "Python"], top_n=3)
    assert result.height == 3
    assert "recommended_skills" in result.columns

