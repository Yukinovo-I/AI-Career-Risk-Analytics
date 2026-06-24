from __future__ import annotations

import csv
import random
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
REFERENCE_DIR = ROOT / "data" / "reference"


OCCUPATIONS = [
    {
        "title": "Data Analyst",
        "base_salary": 72000,
        "growth": 0.08,
        "skills": ["sql", "python", "excel", "tableau", "statistics", "business analysis"],
    },
    {
        "title": "Risk Analyst",
        "base_salary": 78000,
        "growth": 0.12,
        "skills": ["sql", "python", "credit risk", "statistics", "model validation", "excel"],
    },
    {
        "title": "Software Engineer",
        "base_salary": 105000,
        "growth": 0.10,
        "skills": ["python", "java", "cloud", "system design", "sql", "git"],
    },
    {
        "title": "Machine Learning Engineer",
        "base_salary": 118000,
        "growth": 0.18,
        "skills": ["python", "machine learning", "pytorch", "mlops", "cloud", "sql"],
    },
    {
        "title": "Data Engineer",
        "base_salary": 103000,
        "growth": 0.17,
        "skills": ["sql", "python", "spark", "airflow", "cloud", "data modeling"],
    },
    {
        "title": "Quant Analyst",
        "base_salary": 112000,
        "growth": 0.16,
        "skills": ["python", "statistics", "risk modeling", "sql", "machine learning", "financial modeling"],
    },
    {
        "title": "Business Analyst",
        "base_salary": 70000,
        "growth": 0.05,
        "skills": ["excel", "sql", "power bi", "stakeholder management", "process analysis", "statistics"],
    },
    {
        "title": "Basic Accountant",
        "base_salary": 56000,
        "growth": 0.01,
        "skills": ["excel", "bookkeeping", "erp", "reconciliation", "tax", "reporting"],
    },
    {
        "title": "Data Entry Clerk",
        "base_salary": 42000,
        "growth": -0.02,
        "skills": ["excel", "data entry", "typing", "crm", "quality check", "documentation"],
    },
    {
        "title": "Manual Tester",
        "base_salary": 65000,
        "growth": 0.00,
        "skills": ["manual testing", "test cases", "jira", "excel", "api testing", "documentation"],
    },
    {
        "title": "Financial Analyst",
        "base_salary": 82000,
        "growth": 0.07,
        "skills": ["excel", "sql", "financial modeling", "python", "forecasting", "power bi"],
    },
    {
        "title": "Cybersecurity Analyst",
        "base_salary": 96000,
        "growth": 0.15,
        "skills": ["network security", "python", "siem", "cloud", "risk assessment", "sql"],
    },
]


REFERENCE_ROWS = [
    ["Data Analyst", "15-2051", "Data", 45, 58, 76, 24, 18, "O*NET/BLS-inspired sample"],
    ["Risk Analyst", "13-2099", "Finance/Risk", 38, 48, 80, 20, 15, "O*NET/BLS-inspired sample"],
    ["Software Engineer", "15-1252", "Technology", 28, 62, 84, 16, 17, "O*NET/BLS-inspired sample"],
    ["Machine Learning Engineer", "15-1252", "AI/Technology", 22, 55, 90, 10, 24, "O*NET/BLS-inspired sample"],
    ["Data Engineer", "15-1243", "Data Infrastructure", 24, 50, 88, 12, 23, "O*NET/BLS-inspired sample"],
    ["Quant Analyst", "15-2099", "Finance/Quant", 30, 44, 82, 18, 19, "O*NET/BLS-inspired sample"],
    ["Business Analyst", "13-1111", "Business", 52, 55, 68, 32, 9, "O*NET/BLS-inspired sample"],
    ["Basic Accountant", "13-2011", "Accounting", 70, 66, 48, 52, 2, "O*NET/BLS-inspired sample"],
    ["Data Entry Clerk", "43-9021", "Administration", 86, 72, 30, 70, -7, "O*NET/BLS-inspired sample"],
    ["Manual Tester", "15-1253", "Quality Assurance", 68, 64, 46, 54, 1, "O*NET/BLS-inspired sample"],
    ["Financial Analyst", "13-2051", "Finance", 40, 46, 72, 28, 10, "O*NET/BLS-inspired sample"],
    ["Cybersecurity Analyst", "15-1212", "Cybersecurity", 26, 42, 87, 13, 22, "O*NET/BLS-inspired sample"],
]


MAJOR_ROWS = [
    ["Mathematics", "statistics|python|sql|linear algebra|optimization"],
    ["Statistics", "statistics|python|sql|machine learning|experiment design"],
    ["Computer Science", "python|sql|git|cloud|system design"],
    ["Finance", "excel|sql|financial modeling|risk modeling|python"],
    ["Business", "excel|sql|power bi|stakeholder management|process analysis"],
    ["Accounting", "excel|erp|reconciliation|sql|reporting"],
]


def main() -> None:
    random.seed(20260624)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)

    with (RAW_DIR / "jobs_sample.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "job_id",
                "job_title",
                "company",
                "location",
                "country",
                "salary",
                "skills",
                "experience",
                "date_posted",
                "source",
            ]
        )
        job_id = 1
        for year in [2023, 2024, 2025, 2026]:
            for occupation in OCCUPATIONS:
                for idx in range(3):
                    salary = occupation["base_salary"] * ((1 + occupation["growth"]) ** (year - 2023))
                    salary *= random.uniform(0.92, 1.12)
                    skills = occupation["skills"][:]
                    random.shuffle(skills)
                    location = random.choice(["New York", "Shanghai", "Shenzhen", "Singapore", "London", "Remote"])
                    country = {
                        "New York": "US",
                        "Shanghai": "CN",
                        "Shenzhen": "CN",
                        "Singapore": "SG",
                        "London": "UK",
                        "Remote": "Global",
                    }[location]
                    month = random.randint(1, 12)
                    day = random.randint(1, 26)
                    writer.writerow(
                        [
                            f"J{job_id:04d}",
                            occupation["title"],
                            random.choice(["Atlas Analytics", "Northwind Bank", "Nova AI", "BluePeak Tech", "Helio Retail"]),
                            location,
                            country,
                            round(salary, 0),
                            "|".join(skills),
                            random.choice(["entry", "mid", "senior"]),
                            date(year, month, day).isoformat(),
                            "sample_kaggle_style",
                        ]
                    )
                    job_id += 1

    with (REFERENCE_DIR / "occupation_reference.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "occupation",
                "soc_code",
                "occupation_family",
                "repetitive_task_score",
                "ai_exposure_score",
                "future_outlook_score",
                "job_decline_reference_score",
                "demand_growth_pct",
                "source_note",
            ]
        )
        writer.writerows(REFERENCE_ROWS)

    with (REFERENCE_DIR / "major_skill_map.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["major", "recommended_base_skills"])
        writer.writerows(MAJOR_ROWS)


if __name__ == "__main__":
    main()

