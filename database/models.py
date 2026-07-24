"""Normalized relational schema for the job market warehouse."""
from datetime import date, datetime
from sqlalchemy import Column, Date, DateTime, ForeignKey, Numeric, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

job_skills = Table(
    "job_skills", Base.metadata,
    Column("job_id", ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)

class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    industry: Mapped[str | None] = mapped_column(String(120))
    jobs: Mapped[list["Job"]] = relationship(back_populates="company")

class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    province: Mapped[str | None] = mapped_column(String(120))

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)

class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    canonical_name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    jobs: Mapped[list["Job"]] = relationship(secondary=job_skills, back_populates="skills")

class EmploymentType(Base):
    __tablename__ = "employment_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

class ExperienceLevel(Base):
    __tablename__ = "experience_levels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

class Job(Base):
    __tablename__ = "jobs"
    __table_args__ = (UniqueConstraint("source", "source_job_id", name="uq_source_job"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(80), index=True)
    source_job_id: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(1000))
    title: Mapped[str] = mapped_column(String(500), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    posted_at: Mapped[date | None] = mapped_column(Date, index=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    employment_type_id: Mapped[int | None] = mapped_column(ForeignKey("employment_types.id"))
    experience_level_id: Mapped[int | None] = mapped_column(ForeignKey("experience_levels.id"))
    company: Mapped[Company] = relationship(back_populates="jobs")
    skills: Mapped[list[Skill]] = relationship(secondary=job_skills, back_populates="jobs")
    salary: Mapped["Salary | None"] = relationship(back_populates="job", uselist=False, cascade="all, delete-orphan")

class Salary(Base):
    __tablename__ = "salaries"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), unique=True)
    min_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    max_amount: Mapped[float | None] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(10), default="PKR")
    period: Mapped[str] = mapped_column(String(20), default="monthly")
    job: Mapped[Job] = relationship(back_populates="salary")
