from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import polars as pl
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .config import DASHBOARD_DIR, DOCS_DIR, PROJECT_ROOT
from .risk_model import CareerRiskModel


def build_figures(model: CareerRiskModel, output_dir: Path = DASHBOARD_DIR / "figures") -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scores = model.occupation_scores()
    skill_rank = model.skill_value_ranking().head(12)

    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    risk_path = output_dir / "career_risk_ranking.png"
    top = scores.sort("ai_risk_score", descending=True).head(10)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top["occupation"].to_list(), top["ai_risk_score"].to_list(), color="#C9514A")
    ax.invert_yaxis()
    ax.set_xlabel("AI Risk Score")
    ax.set_title("Career AI Risk Ranking")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(risk_path, dpi=180)
    plt.close(fig)

    demand_path = output_dir / "career_demand_ranking.png"
    demand = scores.sort("future_demand_score").tail(10)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(demand["occupation"].to_list(), demand["future_demand_score"].to_list(), color="#2F7F6F")
    ax.set_xlabel("Future Demand Score")
    ax.set_title("Future Demand Ranking")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(demand_path, dpi=180)
    plt.close(fig)

    skill_path = output_dir / "skill_salary_growth.png"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(skill_rank["skill"].to_list(), skill_rank["salary_growth_pct"].to_list(), color="#4A6FA5")
    ax.invert_yaxis()
    ax.set_xlabel("Salary Growth %")
    ax.set_title("Skill Value Growth")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(skill_path, dpi=180)
    plt.close(fig)

    return {"risk": risk_path, "demand": demand_path, "skills": skill_path}


def build_markdown_report(model: CareerRiskModel, output_path: Path = DOCS_DIR / "report.md") -> Path:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    scores = model.occupation_scores()
    skill_rank = model.skill_value_ranking().head(10)
    student = model.simulate_student("Mathematics", ["SQL", "Python"], top_n=5)

    lines = [
        "# AI时代大学生就业竞争力分析与职业风险预测系统",
        "",
        "## 项目摘要",
        "",
        "本项目将职位数据、O*NET职业技能框架和薪资/岗位趋势合并为一个可解释的职业风险评分系统。",
        "模型面向AI时代的职业选择场景，输出职业AI风险、未来需求、技能价值排名和技能投资建议。",
        "",
        "## 模型公式",
        "",
        "`AI Risk Score = 40% repetitive task + 30% AI exposure + 20% salary stagnation + 10% job decline`",
        "",
        "## 职业风险排名",
        "",
        _markdown_table(scores.select("occupation", "ai_risk_score", "future_demand_score", "risk_band").head(12)),
        "",
        "## 技能价值排名",
        "",
        _markdown_table(skill_rank.select("skill", "salary_growth_pct", "last_salary_usd", "posting_count")),
        "",
        "## 个人职业模拟器示例",
        "",
        "输入：专业 Mathematics；技能 SQL、Python。",
        "",
        _markdown_table(
            student.select(
                "occupation",
                "student_fit_score",
                "ai_risk_score",
                "future_demand_score",
                "recommended_skills",
            )
        ),
        "",
        "## 商业价值",
        "",
        "- 学生端：判断职业风险、规划技能投资顺序。",
        "- 学校端：识别课程与市场需求错位，优化就业指导。",
        "- 企业端：观察岗位能力迁移，辅助人才培养与招聘策略。",
        "",
        "## 数据边界",
        "",
        "本版本使用可复现实验数据集验证方法链路。严肃预测应替换为当前、可追溯、合规获取的职位、O*NET、BLS和招聘平台数据。",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def build_pdf_report(model: CareerRiskModel, output_path: Path = PROJECT_ROOT / "report.pdf") -> Path:
    figures = build_figures(model)
    build_markdown_report(model)
    scores = model.occupation_scores().head(10)
    skill_rank = model.skill_value_ranking().head(8)
    student = model.simulate_student("Mathematics", ["SQL", "Python"], top_n=5)

    font_name = _register_cjk_font()
    styles = getSampleStyleSheet()
    for style_name in ["Title", "Heading1", "Heading2", "BodyText"]:
        styles[style_name].fontName = font_name
    styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName=font_name, fontSize=8.8, leading=11))
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName=font_name,
            spaceBefore=10,
            spaceAfter=6,
        )
    )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
    )

    story = [
        Paragraph("AI Career Risk Analytics", styles["Title"]),
        Paragraph("AI时代大学生就业竞争力分析与职业风险预测系统", styles["Heading2"]),
        Paragraph(
            "This report integrates job-posting signals, occupation skill references, salary trend analysis, "
            "and a transparent risk-scoring model for student career planning.",
            styles["BodyText"],
        ),
        Spacer(1, 0.25 * cm),
        Paragraph("Model", styles["Section"]),
        Paragraph(
            "AI Risk Score = 40% repetitive task + 30% AI exposure + 20% salary stagnation + 10% job decline.",
            styles["BodyText"],
        ),
        Paragraph("Career Risk Ranking", styles["Section"]),
        _dataframe_table(scores.select("occupation", "ai_risk_score", "future_demand_score", "risk_band"), font_name),
        Spacer(1, 0.2 * cm),
        Image(str(figures["risk"]), width=16 * cm, height=8.8 * cm),
        PageBreak(),
        Paragraph("Skill Value Ranking", styles["Section"]),
        _dataframe_table(skill_rank.select("skill", "salary_growth_pct", "last_salary_usd", "posting_count"), font_name),
        Spacer(1, 0.2 * cm),
        Image(str(figures["skills"]), width=16 * cm, height=8.8 * cm),
        Paragraph("Student Simulator", styles["Section"]),
        Paragraph("Input: Major = Mathematics; Skills = SQL, Python.", styles["BodyText"]),
        _dataframe_table(
            student.select("occupation", "student_fit_score", "ai_risk_score", "future_demand_score", "recommended_skills"),
            font_name,
        ),
        Paragraph("Business Value", styles["Section"]),
        Paragraph(
            "Students can prioritize resilient career paths and skills. Universities can compare curriculum supply "
            "with demand signals. Employers can track role transformation under AI adoption.",
            styles["BodyText"],
        ),
        Paragraph("Data Boundary", styles["Section"]),
        Paragraph(
            "This version uses a reproducible demonstration dataset to validate the workflow. Serious forecasting "
            "should replace it with current, traceable, and compliant labor-market data.",
            styles["Small"],
        ),
    ]
    doc.build(story)
    return output_path


def _dataframe_table(frame: pl.DataFrame, font_name: str) -> Table:
    data = [frame.columns] + [[_format_cell(value) for value in row.values()] for row in frame.to_dicts()]
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 7.2),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def _markdown_table(frame: pl.DataFrame) -> str:
    rows = [[str(column) for column in frame.columns]]
    rows.extend([[_format_markdown_cell(value) for value in row.values()] for row in frame.to_dicts()])
    widths = [max(len(row[idx]) for row in rows) for idx in range(len(rows[0]))]
    lines = [
        "| " + " | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(rows[0])) + " |",
        "| " + " | ".join("-" * width for width in widths) + " |",
    ]
    for row in rows[1:]:
        lines.append("| " + " | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(row)) + " |")
    return "\n".join(lines)


def _format_cell(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.2f}"
    return "" if value is None else str(value)


def _format_markdown_cell(value: object) -> str:
    return _format_cell(value).replace("|", ", ")


def _register_cjk_font() -> str:
    candidates = [
        Path("C:/Windows/Fonts/NotoSansSC-VF.ttf"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
    ]
    for path in candidates:
        if path.exists():
            pdfmetrics.registerFont(TTFont("CareerCJK", str(path)))
            return "CareerCJK"
    return "Helvetica"
