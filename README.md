# AI-Career-Risk-Analytics

AI时代大学生就业竞争力分析与职业风险预测系统。

随着 AI 改变就业市场，本项目分析全球/中国大学生技能、专业、薪资与岗位需求变化，构建职业竞争力评分模型，帮助学生判断未来职业风险和技能投资方向。

## 项目亮点

- **数据分析**：清洗职位、技能、薪资和职业参考数据，输出职业风险、技能价值和个人推荐结果。
- **风控思维**：把职业风险拆成重复性任务、AI暴露、薪资停滞、岗位下降四个可解释维度。
- **数学统计背景**：使用薪资增长率、需求得分、标准化评分和加权模型。
- **AI时代热点**：关注AI替代风险、技能升级和职业韧性。
- **商业价值**：服务学生择业、学校就业指导、企业人才策略。

## 数据来源与边界

仓库默认提供一套可复现样例数据，字段结构模拟 Kaggle 职位数据，适合开箱运行和作品集展示。真实项目可替换为：

- Kaggle职位数据：如 Data Science Job Postings with Salaries (2025)。
- O*NET职业技能数据库：O*NET 30.3 提供 Software Skills、Essential Skills、Occupation Data 等文件。
- BLS职业展望：用于校准职业薪资、就业增长和岗位展望。
- LinkedIn / Indeed：建议使用官方API、学校/企业合规数据导出、数据供应商或公开研究数据，不把未授权爬虫作为默认路径。

## 项目结构

```text
AI-Career-Risk-Analytics
├── data
│   ├── raw
│   ├── reference
│   ├── processed
│   └── warehouse
├── sql
│   ├── schema.sql
│   └── analysis.sql
├── polars_pipeline
├── dashboard
│   └── index.html
├── scripts
│   ├── make_sample_data.py
│   ├── run_pipeline.py
│   ├── download_sources.py
│   └── upload_to_github.ps1
├── tests
├── docs
├── report.pdf
└── README.md
```

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\run_pipeline.py
pytest -q
```

运行后会生成：

- `data/processed/jobs_clean.csv`
- `data/processed/job_skills.csv`
- `data/processed/occupation_risk_scores.csv`
- `data/warehouse/career_risk.duckdb`
- `dashboard/dashboard_data.json`
- `dashboard/figures/*.png`
- `docs/report.md`
- `report.pdf`

Dashboard 打开方式：

```powershell
python -m http.server 8000 -d dashboard
```

浏览器访问 `http://localhost:8000`。

## Step 1 数据清洗：Polars Lazy API

核心逻辑位于 `polars_pipeline/clean_jobs.py`：

```python
df = (
    pl.scan_csv("data/raw/jobs_sample.csv")
    .filter(pl.col("salary").is_not_null())
    .with_columns(pl.col("skills").str.to_lowercase())
    .collect()
)
```

项目实际会进一步拆分技能字段，生成 `jobs_clean.csv`、`job_skills.csv`、`salary_history.csv` 和 `skill_salary_metrics.csv`。

## Step 2 SQL数据仓库设计

使用 DuckDB，本地文件为 `data/warehouse/career_risk.duckdb`。

核心表：

- `jobs`：职位、公司、地点、薪资、经验、发布时间。
- `skills`：岗位-技能明细表。
- `salary_history`：职业年度薪资历史。
- `occupation`：职业参考表，包含AI风险相关解释变量。

示例问题：

```sql
SELECT
    skill,
    ROUND(AVG(salary_usd), 2) AS avg_salary_usd,
    COUNT(*) AS job_skill_mentions
FROM skills
GROUP BY skill
ORDER BY avg_salary_usd DESC;
```

完整 SQL 见 `sql/analysis.sql`。

## Step 3 职业风险评分模型

模型公式：

```text
AI Risk Score =
40% repetitive task
+ 30% AI exposure
+ 20% salary stagnation
+ 10% job decline
```

示例输出：

```text
职业：Data Analyst
AI Risk：中等
Future Demand：较高
Recommended Skills：SQL, Python, Machine Learning, Statistics
```

个人职业模拟器位于 `CareerRiskModel.simulate_student()`，输入专业和已掌握技能，输出推荐职业和技能缺口。

## Step 4 Dashboard

`dashboard/index.html` 包含三页：

- Page 1：未来就业地图，展示低风险/高需求职业与高风险职业。
- Page 2：技能价值排名，展示技能薪资增长。
- Page 3：个人职业模拟器，展示数学/统计/计算机/金融等专业的职业建议。

## 上传 GitHub

目标仓库：

```text
https://github.com/Yukinovo-I/AI-Career-Risk-Analytics
```

当前机器如果仍登录旧账号，需要先切换 GitHub CLI 登录：

```powershell
gh auth logout -h github.com -u Yukino-O
gh auth login -h github.com
```

登录完成后运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\upload_to_github.ps1 -Owner Yukinovo-I -RepoName AI-Career-Risk-Analytics
```

## 作品集定位

这是一个数据分析与风险建模作品集项目，强调数据管道、SQL仓库、可解释评分、Dashboard 和报告交付。样例数据用于演示方法论，不应直接当作真实就业预测结论。
