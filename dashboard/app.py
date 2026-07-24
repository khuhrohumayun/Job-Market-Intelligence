"""Interactive Streamlit dashboard for the job-market warehouse."""
import sys
from pathlib import Path

import plotly.express as px
import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
from analysis.queries import (
    hiring_by_city, job_explorer, kpis, monthly_hiring_trend, role_demand,
    source_summary, top_companies, top_skills,
)
from ml.forecast import forecast_daily_demand
from analysis.queries import hiring_trend

st.set_page_config(page_title="Pakistan Job Market Intelligence", page_icon=":bar_chart:", layout="wide")
st.title("Pakistan Job Market Intelligence")
st.caption("Explore hiring demand, skill signals, and location patterns.")

try:
    skills = top_skills()
    cities = hiring_by_city()
    monthly_trend = monthly_hiring_trend()
    daily_trend = hiring_trend()
    jobs = job_explorer()
    sources = source_summary()
    companies = top_companies()
    roles = role_demand()
    summary = kpis().iloc[0]
except Exception:
    st.error("Database unavailable. Run `python scripts/bootstrap.py` and `python scripts/load_sample.py` first.")
    st.stop()

st.caption("Data sources: " + ", ".join(f"{row.source} ({row.jobs:,})" for row in sources.itertuples()))

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
kpi_1.metric("Job postings", f"{summary.total_jobs:,}")
kpi_2.metric("Companies", f"{summary.companies:,}")
kpi_3.metric("Cities", f"{summary.cities:,}")
kpi_4.metric("Tracked skills", f"{len(skills):,}")

st.subheader("Market overview")
left, right = st.columns(2)
with left:
    st.plotly_chart(
        px.bar(skills.head(12).sort_values("jobs"), x="jobs", y="skill", orientation="h", title="Most requested skills", template="plotly_dark"),
        use_container_width=True,
    )
with right:
    st.plotly_chart(
        px.bar(roles.sort_values("jobs"), x="jobs", y="title", orientation="h", title="Demand by job role", template="plotly_dark"),
        use_container_width=True,
    )

left, right = st.columns(2)
with left:
    st.plotly_chart(
        px.line(monthly_trend, x="month", y="jobs", markers=True, title="Monthly hiring trend", template="plotly_dark"),
        use_container_width=True,
    )
with right:
    st.plotly_chart(
        px.pie(cities.head(8), names="city", values="jobs", hole=0.5, title="Hiring share by city", template="plotly_dark"),
        use_container_width=True,
    )

left, right = st.columns(2)
with left:
    st.plotly_chart(
        px.bar(companies.head(10).sort_values("jobs"), x="jobs", y="company", orientation="h", title="Top hiring companies", template="plotly_dark"),
        use_container_width=True,
    )
with right:
    st.plotly_chart(
        px.bar(cities.head(8).sort_values("jobs"), x="jobs", y="city", orientation="h", title="Top hiring cities", template="plotly_dark"),
        use_container_width=True,
    )

forecast, mae = forecast_daily_demand(daily_trend)
if not forecast.empty:
    st.subheader("Forecast")
    st.plotly_chart(
        px.line(forecast, x="posted_at", y="predicted_jobs", title="30-day hiring-demand baseline forecast", template="plotly_dark"),
        use_container_width=True,
    )
    if mae is not None:
        st.caption(f"Validation MAE: {mae:.2f} postings/day (Ridge baseline)")

st.subheader("Job explorer")
filter_1, filter_2 = st.columns(2)
with filter_1:
    selected_cities = st.multiselect("Cities", sorted(jobs["city"].dropna().unique()))
with filter_2:
    selected_roles = st.multiselect("Roles", sorted(jobs["title"].dropna().unique()))
search_text = st.text_input("Search job title or company")

filtered = jobs.copy()
if selected_cities:
    filtered = filtered[filtered["city"].isin(selected_cities)]
if selected_roles:
    filtered = filtered[filtered["title"].isin(selected_roles)]
if search_text:
    match = filtered["title"].str.contains(search_text, case=False, na=False) | filtered["company"].str.contains(search_text, case=False, na=False)
    filtered = filtered[match]
st.caption(f"Showing {len(filtered):,} of {len(jobs):,} jobs")
st.download_button("Export filtered CSV", filtered.to_csv(index=False), "filtered_jobs.csv", "text/csv")
st.dataframe(filtered, use_container_width=True, hide_index=True)
