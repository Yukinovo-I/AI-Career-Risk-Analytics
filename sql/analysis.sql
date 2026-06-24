-- 1. 哪些技能当前薪资最高？
SELECT
    skill,
    ROUND(AVG(salary_usd), 2) AS avg_salary_usd,
    COUNT(*) AS job_skill_mentions
FROM skills
GROUP BY skill
HAVING COUNT(*) >= 5
ORDER BY avg_salary_usd DESC;

-- 2. 哪些技能薪资增长最快？
WITH yearly AS (
    SELECT
        skill,
        posting_year,
        AVG(salary_usd) AS avg_salary_usd,
        COUNT(*) AS mentions
    FROM skills
    GROUP BY skill, posting_year
),
bounds AS (
    SELECT
        skill,
        MIN(posting_year) AS first_year,
        MAX(posting_year) AS last_year,
        SUM(mentions) AS total_mentions
    FROM yearly
    GROUP BY skill
),
growth AS (
    SELECT
        b.skill,
        b.first_year,
        b.last_year,
        f.avg_salary_usd AS first_salary_usd,
        l.avg_salary_usd AS last_salary_usd,
        ROUND((l.avg_salary_usd - f.avg_salary_usd) / f.avg_salary_usd * 100, 2) AS salary_growth_pct,
        b.total_mentions
    FROM bounds b
    JOIN yearly f ON b.skill = f.skill AND b.first_year = f.posting_year
    JOIN yearly l ON b.skill = l.skill AND b.last_year = l.posting_year
)
SELECT *
FROM growth
WHERE total_mentions >= 5
ORDER BY salary_growth_pct DESC, last_salary_usd DESC;

-- 3. 哪些职业AI替代风险高？
WITH salary_growth AS (
    SELECT
        job_title AS occupation,
        MIN(posting_year) AS first_year,
        MAX(posting_year) AS last_year
    FROM salary_history
    GROUP BY job_title
),
growth AS (
    SELECT
        g.occupation,
        ROUND((last.avg_salary_usd - first.avg_salary_usd) / first.avg_salary_usd * 100, 2) AS salary_growth_pct
    FROM salary_growth g
    JOIN salary_history first
        ON g.occupation = first.job_title AND g.first_year = first.posting_year
    JOIN salary_history last
        ON g.occupation = last.job_title AND g.last_year = last.posting_year
),
scored AS (
    SELECT
        o.occupation,
        o.repetitive_task_score,
        o.ai_exposure_score,
        COALESCE(g.salary_growth_pct, 0) AS salary_growth_pct,
        100 - LEAST(GREATEST((COALESCE(g.salary_growth_pct, 0) + 5) / 30 * 100, 0), 100) AS salary_stagnation_score,
        100 - o.future_outlook_score AS job_decline_score,
        ROUND(
            0.40 * o.repetitive_task_score
            + 0.30 * o.ai_exposure_score
            + 0.20 * (100 - LEAST(GREATEST((COALESCE(g.salary_growth_pct, 0) + 5) / 30 * 100, 0), 100))
            + 0.10 * (100 - o.future_outlook_score),
            2
        ) AS ai_risk_score
    FROM occupation o
    LEFT JOIN growth g ON o.occupation = g.occupation
)
SELECT *
FROM scored
ORDER BY ai_risk_score DESC;

-- 4. 职业竞争力：风险低、需求高、薪资高的职业。
SELECT
    j.job_title,
    ROUND(AVG(j.salary_usd), 2) AS avg_salary_usd,
    COUNT(*) AS postings,
    o.future_outlook_score,
    o.demand_growth_pct
FROM jobs j
JOIN occupation o ON j.job_title = o.occupation
GROUP BY j.job_title, o.future_outlook_score, o.demand_growth_pct
ORDER BY o.future_outlook_score DESC, avg_salary_usd DESC;

