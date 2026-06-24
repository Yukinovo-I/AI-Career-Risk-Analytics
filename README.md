# AI-Career-Risk-Analytics

[![tests](https://github.com/Yukinovo-I/AI-Career-Risk-Analytics/actions/workflows/tests.yml/badge.svg)](https://github.com/Yukinovo-I/AI-Career-Risk-Analytics/actions/workflows/tests.yml)
[![Live Dashboard](https://img.shields.io/badge/live-dashboard-2f7f6f)](https://yukinovo-i.github.io/AI-Career-Risk-Analytics/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

AI-Career-Risk-Analytics is a labor-market analytics project for understanding how AI changes graduate employability, skill premiums, and occupational risk.

The project combines job-posting style data, occupation-level skill references, salary trends, and a transparent risk-scoring model. It turns a broad question - "which careers remain competitive in an AI-shaped labor market?" - into a reproducible analytics pipeline, SQL warehouse, interactive dashboard, and report.

## Live Demo

Interactive dashboard:

https://yukinovo-i.github.io/AI-Career-Risk-Analytics/

Project report:

[report.pdf](report.pdf)

## What The Project Does

- Scores occupations by AI replacement risk, future demand, and salary momentum.
- Ranks skills by salary growth and labor-market value.
- Simulates career fit from a student's major and current skill set.
- Shows which skills are worth investing in for data, risk, finance, and technology roles.
- Keeps the scoring model interpretable instead of treating career risk as a black box.

## Why It Matters

AI is changing entry-level work unevenly. Some roles absorb AI as a productivity tool, while others are exposed because they rely heavily on repetitive, rule-based, or easily automated tasks.

This project frames career planning as a risk-analysis problem:

- **Exposure**: How directly can current AI systems perform or accelerate the work?
- **Resilience**: Does the role require judgment, domain knowledge, infrastructure ownership, or complex problem solving?
- **Market signal**: Are salaries and postings moving up or stagnating?
- **Skill strategy**: Which skills improve career optionality across multiple paths?

## Core Outputs

| Output | Description |
| --- | --- |
| Career risk score | Weighted AI risk score for each occupation |
| Future demand score | Demand outlook combining role outlook, risk, and posting volume |
| Skill value ranking | Salary-growth ranking for technical and analytical skills |
| Student simulator | Career-fit recommendations from major and skills |
| SQL warehouse | DuckDB tables for repeatable analysis |
| Report | PDF summary of the model, results, and business interpretation |

## Methodology

The risk model is intentionally transparent:

```text
AI Risk Score =
40% repetitive task exposure
+ 30% AI exposure
+ 20% salary stagnation
+ 10% job decline pressure
```

The score is not intended to be a universal truth. It is a structured decision tool that makes assumptions explicit and easy to challenge.

## Data Sources

The repository includes a reproducible demonstration dataset so the pipeline, dashboard, and tests can run without private credentials. The schema mirrors the public data sources the model is designed to integrate:

- Kaggle-style job postings: job title, company, location, salary, skills, experience, date posted.
- O*NET occupation data: skill requirements, technology usage, occupational descriptors.
- BLS occupation outlook data: wage and employment-growth signals.
- Compliant job-platform exports or public research datasets for LinkedIn/Indeed-style demand signals.

The included dataset is for method demonstration. Real forecasting should replace it with current, documented, and legally usable labor-market data.

## Architecture

```text
AI-Career-Risk-Analytics
|-- data
|   |-- raw                 # demonstration job-posting input
|   |-- reference           # occupation and major-skill reference data
|   |-- processed           # generated analytical tables
|   `-- warehouse           # DuckDB warehouse
|-- sql
|   |-- schema.sql
|   `-- analysis.sql
|-- polars_pipeline
|   |-- clean_jobs.py       # Polars Lazy API data cleaning
|   |-- warehouse.py        # DuckDB table build
|   |-- risk_model.py       # career risk and fit scoring
|   |-- dashboard.py        # dashboard JSON export
|   `-- reporting.py        # figures, Markdown report, PDF report
|-- dashboard
|   |-- index.html
|   |-- dashboard_data.json
|   `-- figures
|-- scripts
|   |-- make_sample_data.py
|   |-- run_pipeline.py
|   `-- download_sources.py
|-- tests
|-- docs
|-- report.pdf
`-- README.md
```

## Reproduce The Analysis

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest -q
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\run_pipeline.py
pytest -q
```

Generated artifacts include:

- `data/processed/occupation_risk_scores.csv`
- `data/processed/skill_value_ranking.csv`
- `data/processed/student_simulator_demo.csv`
- `data/warehouse/career_risk.duckdb`
- `dashboard/dashboard_data.json`
- `dashboard/figures/*.png`
- `docs/report.md`
- `report.pdf`

## Example Findings From The Demonstration Dataset

- High-risk occupations tend to have high repetitive-task intensity and weak salary momentum, such as data entry and manual testing.
- Lower-risk, high-demand paths cluster around infrastructure, security, machine learning, quantitative analysis, and risk modeling.
- Skills with strong upside are not just programming languages. Data engineering, MLOps, cloud, cybersecurity, model validation, and risk modeling improve resilience because they transfer across roles.
- A mathematics background becomes more marketable when paired with SQL, Python, statistics, machine learning, and domain-specific modeling.

## Business Value

For students, the system turns vague career anxiety into concrete skill-investment decisions.

For universities, it provides a way to compare curriculum content with changing market demand.

For employers, it highlights where roles are being redesigned by AI and which capabilities should be cultivated internally.

## Limitations

- The included dataset is a demonstration dataset, not a real-time labor-market feed.
- Salary and posting trends should be refreshed before making serious career or curriculum decisions.
- AI exposure is modeled as a structured proxy; it should be recalibrated with expert review and current task-level evidence.
- LinkedIn and Indeed-style data should be acquired through compliant exports, partnerships, APIs, or public research datasets.

## Roadmap

- Add real O*NET ingestion for Skills, Technology Skills, and Occupation Data files.
- Add BLS employment projections ingestion.
- Add regional views for China, the United States, and global remote roles.
- Add model-calibration notebooks comparing risk scores with expert labels.
- Add a richer career simulator with course recommendations and learning-path sequencing.
