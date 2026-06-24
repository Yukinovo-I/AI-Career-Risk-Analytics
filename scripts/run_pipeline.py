from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from polars_pipeline.clean_jobs import clean_jobs
from polars_pipeline.dashboard import build_dashboard_data
from polars_pipeline.reporting import build_markdown_report, build_pdf_report
from polars_pipeline.risk_model import CareerRiskModel
from polars_pipeline.warehouse import build_warehouse


def ensure_sample_data() -> None:
    jobs_path = ROOT / "data" / "raw" / "jobs_sample.csv"
    occupation_path = ROOT / "data" / "reference" / "occupation_reference.csv"
    if jobs_path.exists() and occupation_path.exists():
        return
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_sample_data.py")], check=True)


def main() -> None:
    ensure_sample_data()
    print("1/5 Polars cleaning...")
    outputs = clean_jobs()
    for name, path in outputs.items():
        print(f"  {name}: {path.relative_to(ROOT)}")

    print("2/5 DuckDB warehouse...")
    warehouse_path = build_warehouse()
    print(f"  warehouse: {warehouse_path.relative_to(ROOT)}")

    print("3/5 Risk model outputs...")
    model = CareerRiskModel()
    scores_path = ROOT / "data" / "processed" / "occupation_risk_scores.csv"
    skill_path = ROOT / "data" / "processed" / "skill_value_ranking.csv"
    simulator_path = ROOT / "data" / "processed" / "student_simulator_demo.csv"
    model.occupation_scores().write_csv(scores_path)
    model.skill_value_ranking().write_csv(skill_path)
    model.simulate_student("Mathematics", ["SQL", "Python"]).write_csv(simulator_path)
    print(f"  scores: {scores_path.relative_to(ROOT)}")
    print(f"  skills: {skill_path.relative_to(ROOT)}")
    print(f"  simulator: {simulator_path.relative_to(ROOT)}")

    print("4/5 Dashboard data and report...")
    dashboard_path = build_dashboard_data(model)
    markdown_path = build_markdown_report(model)
    pdf_path = build_pdf_report(model)
    print(f"  dashboard data: {dashboard_path.relative_to(ROOT)}")
    print(f"  markdown report: {markdown_path.relative_to(ROOT)}")
    print(f"  pdf report: {pdf_path.relative_to(ROOT)}")

    print("5/5 Done.")


if __name__ == "__main__":
    main()

