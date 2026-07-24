# Pakistan Job Market Intelligence Platform

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **An enterprise-grade analytics platform for analyzing Pakistani job-market demand.** This project demonstrates production-ready patterns for modular web scraping, ETL pipelines, normalized relational data warehouses, NLP skill extraction, time-series forecasting, and interactive analytics dashboards.

## 🎯 Project Highlights

This is a **full-stack data engineering & analytics project** showcasing:

- **Modular Web Scraping**: Extensible adapter-based architecture for multiple job portals
- **Production ETL**: Idempotent transformations with data validation and normalization
- **Relational Warehouse**: SQLAlchemy ORM with MySQL/SQLite support and proper indexing strategy
- **NLP Processing**: Explainable skill taxonomy and extraction from job descriptions
- **ML Forecasting**: Time-series demand predictions with Ridge baseline and MAE validation
- **Interactive Dashboard**: Streamlit analytics UI with real-time filtering and visualizations
- **Enterprise Practices**: Modular design, comprehensive error handling, Alembic migrations, test coverage

## 📊 Architecture Overview

```
Job Portals → Scraper Adapters → Raw JSONL (Append-only) 
    → ETL Validation → Normalized MySQL/SQLite 
    → Analytics Queries + NLP Processing + ML Models
    → Streamlit Interactive Dashboard
```

The platform follows a **lambda-architecture pattern** for auditability and reprocessing capability.

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Raw JSONL Layer** | Immutable source records enable debugging, reprocessing, and audit trails |
| **Idempotent ETL** | Unique `(source, source_job_id)` key prevents duplicates on re-runs |
| **Normalized Schema** | Lookup tables (companies, skills, cities) reduce storage and enable consistency |
| **Many-to-Many Bridge** | `job_skills` table handles N:N relationships efficiently |
| **Ridge ML Baseline** | Explainable model; use seasonal/ARIMA only after sufficient historical data |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.12 or 3.13** (64-bit)
- **Git**
- Optional: **Docker** & **Docker Compose** (for MySQL)

### Local Setup (SQLite - Zero Configuration)

```powershell
# Clone and navigate
git clone https://github.com/YOUR_USERNAME/job-market-intelligence.git
cd job-market-intelligence

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database and load sample data
python scripts/bootstrap.py
python scripts/load_sample.py

# Launch dashboard
streamlit run dashboard/app.py
```

Visit `http://localhost:8501` to explore the dashboard.

### Production Setup (MySQL)

```powershell
# Start MySQL container
docker compose up -d mysql

# Install MySQL connector
pip install cryptography

# Configure database connection
# Edit .env and set: DATABASE_URL=mysql+pymysql://jobintel:change_me@localhost:3306/job_market

# Bootstrap and load data
python scripts/bootstrap.py
python scripts/load_sample.py
```

---

## 📁 Repository Structure

```
project/
├── scraper/              # Web scraping framework
│   ├── base.py          # Abstract base adapter
│   ├── contracts.py     # Data transfer objects & validation
│   └── source_registry.py # Plugin discovery system
├── etl/                 # ETL transformations
│   ├── pipeline.py      # Orchestration logic
│   └── transform.py     # Data standardization
├── database/            # Data persistence layer
│   ├── models.py        # SQLAlchemy ORM schemas
│   ├── repository.py    # Data access patterns
│   └── migrations/      # Alembic schema versions
├── nlp/                 # Natural language processing
│   └── skills.py        # Skill extraction & canonicalization
├── ml/                  # Machine learning
│   └── forecast.py      # Demand forecasting models
├── analysis/            # Analytics queries
│   └── queries.py       # Warehouse SQL queries
├── dashboard/           # Streamlit presentation
│   └── app.py          # Interactive UI
├── tests/               # Test suite
│   ├── test_transform.py
│   └── test_source_registry.py
└── docs/                # Documentation
    └── architecture.md  # Detailed design docs
```

---

## 🔧 Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Data Collection** | BeautifulSoup4, Requests, Tenacity (retry logic) |
| **ETL & Processing** | Pandas, NumPy, SQLAlchemy 2.0, Alembic |
| **Database** | MySQL 8.0, SQLite, PyMySQL |
| **NLP** | spaCy, scikit-learn (skill canonicalization) |
| **ML** | scikit-learn (Ridge regression, MAE validation) |
| **Analytics** | Pandas aggregations, time-series operations |
| **Visualization** | Streamlit, Plotly (interactive charts) |
| **DevOps** | Docker, Docker Compose |
| **Testing** | pytest |

---

## 📈 Features

### Dashboard Capabilities
- **Market Overview**: Top skills, job roles, hiring trends, company rankings
- **Trend Analysis**: Monthly/daily hiring demand with forecasting
- **Geographic Insights**: Hiring distribution by city
- **Job Explorer**: Filter by city, role, and keywords with CSV export
- **KPIs**: Real-time metrics (total jobs, companies, cities, tracked skills)
- **30-Day Forecast**: Demand baseline prediction with validation metrics

### Analytics Queries
- `top_skills()` - Most requested skills ranked by frequency
- `hiring_by_city()` - Job distribution across cities
- `hiring_trend()` - Daily/monthly job posting trends
- `top_companies()` - Leading employers by job count
- `role_demand()` - Job titles ranked by availability
- `kpis()` - High-level market metrics

### Data Pipeline
- Configurable multi-source scraping (extensible adapter pattern)
- Schema validation and error handling
- Idempotent loading (no duplicates)
- Skill synonym normalization (MySQL → SQL)

---

## 🧪 Testing

```powershell
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_transform.py -v

# Run with coverage
pytest --cov=. tests/
```

Current test coverage includes:
- ✅ ETL transformation logic
- ✅ Source registry discovery
- ✅ Data validation contracts

---

## 📚 Documentation

- **[Architecture Deep Dive](docs/architecture.md)**: Data model, normalization strategy, scaling decisions, security best practices
- **[Database Schema](database/models.py)**: SQLAlchemy ORM definitions
- **[ETL Pipeline](etl/pipeline.py)**: End-to-end data transformation logic

---

## 🔐 Security & Compliance

- ✅ Environment variables for sensitive configuration (`.env` not committed)
- ✅ Parameterized queries (SQLAlchemy ORM prevents SQL injection)
- ✅ Least-privilege database users
- ✅ TLS support for remote database connections
- ✅ Source-specific rate limiting in scrapers
- ✅ Respect for portal terms of service and `robots.txt`

**Important**: Always obtain explicit permission before scraping any website and review their terms of service.

---

## 🎓 Learning Value

This project demonstrates:
- 🏗️ **Scalable Architecture**: Modular design supports adding new data sources and features
- 🔄 **ETL Best Practices**: Idempotency, validation, error handling
- 📊 **Data Warehousing**: Normalized schema, strategic indexing, query optimization
- 🤖 **ML Integration**: Time-series forecasting, model evaluation metrics
- 🎨 **Analytics UI**: Real-time filtering, responsive visualizations
- ✅ **Testing & Quality**: Regression tests, type safety, logging
- 🐳 **DevOps**: Docker containerization, multi-database support

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Add new job portal adapters
- [ ] Implement ARIMA/seasonal forecasting models
- [ ] Expand skill taxonomy
- [ ] Add unit tests for NLP module
- [ ] Optimize large-scale data loading
- [ ] Dashboard mobile responsiveness

**To contribute**:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built as a demonstration of production-grade data engineering practices.

**Connect**: [LinkedIn](#) | [Portfolio](#) | [GitHub](#)

---

## 📞 Support

- 📖 Check the [architecture documentation](docs/architecture.md)
- 🐛 Open an issue for bugs or feature requests
- 💬 Discussions welcome for design questions

---

## Data collection policy

This repository deliberately ships no active portal scraper. Before implementing an adapter, verify written permission, terms of service, robots policy, rate limits, and privacy obligations for that source. Prefer official APIs.

## Testing

```powershell
pytest -q
```

## Generate scalable test data

Generate a deterministic synthetic dataset for performance, dashboard, and ML testing. It is deliberately marked `synthetic_demo` and must not be used for real-market claims.

```powershell
python scripts/generate_synthetic_jobs.py --count 1000
python scripts/load_jsonl.py data/raw/synthetic_jobs.jsonl
```

Source approvals are tracked in `config/sources.yaml`. LinkedIn and Indeed are intentionally not approved for direct scraping. Add a BeautifulSoup source adapter only after you have permission, a terms review, and a robots review.

## Database migrations

For production schema changes, generate and review an Alembic migration, then deploy it:

```powershell
alembic revision --autogenerate -m "add feature"
alembic upgrade head
```

## Roadmap

- Add approved source adapters and scheduling
- Add Alembic revision history and CI workflow
- Add richer salary normalization and data-quality observability
- Compare forecasting models using rolling-origin validation
- Add OpenAI-powered career guidance with consent, redaction, and prompt-injection safeguards

## Screenshots

Add dashboard screenshots here after deploying your first approved data source.
