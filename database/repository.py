"""Idempotent persistence boundary for normalized job records."""
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import Category, City, Company, EmploymentType, ExperienceLevel, Job, Salary, Skill

def _get_or_create(session: Session, model: type, name: str | None):
    if not name:
        return None
    cache = session.info.setdefault("lookup_cache", {})
    cache_key = (model, name)
    if cache_key in cache:
        return cache[cache_key]
    # Skills intentionally use `canonical_name`; all other lookup tables use `name`.
    name_field = "canonical_name" if model is Skill else "name"
    column = getattr(model, name_field)
    record = session.scalar(select(model).where(column == name))
    if record is None:
        record = model(**{name_field: name})
        session.add(record)
        session.flush()
    cache[cache_key] = record
    return record

def upsert_job(session: Session, record: dict) -> Job:
    job = session.scalar(select(Job).where(Job.source == record["source"], Job.source_job_id == record["source_job_id"]))
    company = _get_or_create(session, Company, record["company"])
    city = _get_or_create(session, City, record.get("city"))
    category = _get_or_create(session, Category, record.get("category"))
    employment_type = _get_or_create(session, EmploymentType, record.get("employment_type"))
    experience_level = _get_or_create(session, ExperienceLevel, record.get("experience_level"))
    if job is None:
        job = Job(source=record["source"], source_job_id=record["source_job_id"], url=record["url"], title=record["title"], company=company)
        session.add(job)
    for field in ("url", "title", "description", "posted_at"):
        setattr(job, field, record.get(field))
    job.company, job.city_id, job.category_id = company, getattr(city, "id", None), getattr(category, "id", None)
    job.employment_type_id, job.experience_level_id = getattr(employment_type, "id", None), getattr(experience_level, "id", None)
    job.skills = [_get_or_create(session, Skill, skill) for skill in record.get("skills", [])]
    salary = record.get("salary")
    if salary and (salary.get("min_amount") or salary.get("max_amount")):
        job.salary = Salary(**salary)
    return job
