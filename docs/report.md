# AI时代大学生就业竞争力分析与职业风险预测系统

## 项目摘要

本项目将职位数据、O*NET职业技能框架和薪资/岗位趋势合并为一个可解释的职业风险评分系统。
模型面向AI时代的职业选择场景，输出职业AI风险、未来需求、技能价值排名和技能投资建议。

## 模型公式

`AI Risk Score = 40% repetitive task + 30% AI exposure + 20% salary stagnation + 10% job decline`

## 职业风险排名

| occupation                | ai_risk_score | future_demand_score | risk_band |
| ------------------------- | ------------- | ------------------- | --------- |
| Data Entry Clerk          | 83.00         | 40.75               | High      |
| Manual Tester             | 67.11         | 53.52               | Medium    |
| Basic Accountant          | 63.27         | 55.58               | Medium    |
| Business Analyst          | 42.11         | 71.87               | Low       |
| Financial Analyst         | 39.47         | 74.73               | Low       |
| Data Analyst              | 37.80         | 77.35               | Low       |
| Risk Analyst              | 31.60         | 81.10               | Low       |
| Software Engineer         | 31.40         | 83.35               | Low       |
| Quant Analyst             | 27.00         | 83.35               | Low       |
| Machine Learning Engineer | 26.30         | 87.93               | Low       |
| Data Engineer             | 25.80         | 86.95               | Low       |
| Cybersecurity Analyst     | 24.30         | 86.78               | Low       |

## 技能价值排名

| skill            | salary_growth_pct | last_salary_usd | posting_count |
| ---------------- | ----------------- | --------------- | ------------- |
| mlops            | 57.49             | 191886.33       | 12            |
| pytorch          | 57.49             | 191886.33       | 12            |
| machine learning | 54.30             | 180730.33       | 24            |
| risk modeling    | 50.85             | 169574.33       | 12            |
| data modeling    | 47.79             | 165016.67       | 12            |
| airflow          | 47.79             | 165016.67       | 12            |
| spark            | 47.79             | 165016.67       | 12            |
| cloud            | 47.33             | 160973.17       | 48            |
| siem             | 46.29             | 141242.33       | 12            |
| risk assessment  | 46.29             | 141242.33       | 12            |

## 个人职业模拟器示例

输入：专业 Mathematics；技能 SQL、Python。

| occupation                | student_fit_score | ai_risk_score | future_demand_score | recommended_skills                                  |
| ------------------------- | ----------------- | ------------- | ------------------- | --------------------------------------------------- |
| Quant Analyst             | 69.61             | 27.00         | 83.35               | financial modeling, machine learning, risk modeling |
| Risk Analyst              | 67.68             | 31.60         | 81.10               | credit risk, model validation, excel                |
| Machine Learning Engineer | 65.97             | 26.30         | 87.93               | machine learning, cloud, mlops, pytorch             |
| Cybersecurity Analyst     | 65.86             | 24.30         | 86.78               | cloud, siem, risk assessment, network security      |
| Data Engineer             | 65.63             | 25.80         | 86.95               | airflow, spark, data modeling, cloud                |

## 商业价值

- 学生端：判断职业风险、规划技能投资顺序。
- 学校端：识别课程与市场需求错位，优化就业指导。
- 企业端：观察岗位能力迁移，辅助人才培养与招聘策略。

## 数据边界

本版本使用可复现实验数据集验证方法链路。严肃预测应替换为当前、可追溯、合规获取的职位、O*NET、BLS和招聘平台数据。