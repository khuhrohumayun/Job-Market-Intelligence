# Architecture

The platform uses a layered architecture: scraper adapters collect permitted source data into JSONL raw storage; ETL validates and standardizes it; SQLAlchemy persists normalized entities; analysis and ML read only from the warehouse; Streamlit is a thin presentation layer.

## Normalization

- `companies`, `cities`, `categories`, `skills`, `employment_types`, and `experience_levels` are lookup entities, preventing repeated strings across millions of jobs.
- `job_skills` is a many-to-many bridge because one job requires many skills and each skill appears in many jobs.
- `salaries` is one-to-zero/one with jobs: a salary is optional and its fields do not belong in every job row.
- `(source, source_job_id)` is unique, giving ingestion a stable idempotency key.

Indexes target common filters: job source, title, posting date, company name, and skill name. At scale, land raw files in object storage, use a queue for scraping jobs, and bulk-load staged tables before merging.

## Security and compliance

Never commit `.env`; use least-privilege database users, TLS for remote database connections, parameterized SQL/ORM, and source-specific rate limits. Obtain permission and respect each portal's terms and robots directives before activating an adapter.
