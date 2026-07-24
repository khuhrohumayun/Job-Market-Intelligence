"""Analytics query functions returning dashboard-ready data frames."""
import pandas as pd
from sqlalchemy import text
from database.session import engine

def dataframe(sql: str) -> pd.DataFrame:
    return pd.read_sql(text(sql), engine)

def top_skills() -> pd.DataFrame:
    return dataframe("SELECT s.canonical_name AS skill, COUNT(*) AS jobs FROM job_skills js JOIN skills s ON s.id=js.skill_id GROUP BY s.canonical_name ORDER BY jobs DESC")

def hiring_by_city() -> pd.DataFrame:
    return dataframe("SELECT c.name AS city, COUNT(*) AS jobs FROM jobs j JOIN cities c ON c.id=j.city_id GROUP BY c.name ORDER BY jobs DESC")

def hiring_trend() -> pd.DataFrame:
    return dataframe("SELECT posted_at, COUNT(*) AS jobs FROM jobs WHERE posted_at IS NOT NULL GROUP BY posted_at ORDER BY posted_at")

def monthly_hiring_trend() -> pd.DataFrame:
    # Group in Pandas rather than using SQLite/MySQL-specific date functions.
    trend = hiring_trend()
    if trend.empty:
        return pd.DataFrame(columns=["month", "jobs"])
    trend["posted_at"] = pd.to_datetime(trend["posted_at"])
    return (trend.assign(month=trend["posted_at"].dt.to_period("M").astype(str))
            .groupby("month", as_index=False)["jobs"].sum().sort_values("month"))

def top_companies() -> pd.DataFrame:
    return dataframe("SELECT co.name AS company, COUNT(*) AS jobs FROM jobs j JOIN companies co ON co.id=j.company_id GROUP BY co.name ORDER BY jobs DESC")

def role_demand() -> pd.DataFrame:
    return dataframe("SELECT title, COUNT(*) AS jobs FROM jobs GROUP BY title ORDER BY jobs DESC")

def salary_distribution() -> pd.DataFrame:
    return dataframe("SELECT j.title, c.name AS city, (s.min_amount + s.max_amount) / 2.0 AS monthly_salary FROM salaries s JOIN jobs j ON j.id=s.job_id LEFT JOIN cities c ON c.id=j.city_id WHERE s.min_amount IS NOT NULL AND s.max_amount IS NOT NULL")

def kpis() -> pd.DataFrame:
    return dataframe("SELECT COUNT(*) AS total_jobs, COUNT(DISTINCT company_id) AS companies, COUNT(DISTINCT city_id) AS cities FROM jobs")

def job_explorer() -> pd.DataFrame:
    return dataframe("SELECT j.title, co.name company, ci.name city, j.posted_at, j.url FROM jobs j JOIN companies co ON co.id=j.company_id LEFT JOIN cities ci ON ci.id=j.city_id ORDER BY j.posted_at DESC")

def source_summary() -> pd.DataFrame:
    return dataframe("SELECT source, COUNT(*) AS jobs FROM jobs GROUP BY source ORDER BY jobs DESC")
