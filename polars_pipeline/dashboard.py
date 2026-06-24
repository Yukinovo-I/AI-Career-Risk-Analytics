from __future__ import annotations

import json
from pathlib import Path

from .config import DASHBOARD_DIR
from .risk_model import CareerRiskModel


def build_dashboard_data(model: CareerRiskModel, output_path: Path = DASHBOARD_DIR / "dashboard_data.json") -> Path:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    scores = model.occupation_scores()
    skills = model.skill_value_ranking()
    simulator = model.simulate_student("Mathematics", ["SQL", "Python"], top_n=6)

    payload = {
        "generated_for": "AI Career Risk Analytics",
        "career_scores": scores.to_dicts(),
        "skill_rankings": skills.to_dicts(),
        "student_simulator_demo": simulator.to_dicts(),
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print(build_dashboard_data(CareerRiskModel()))

