"""Dictionary-first skill extraction for explainable, low-cost baseline NLP."""
import re

SKILL_ALIASES = {
    "python": ["python"], "sql": ["sql", "mysql", "postgresql"], "machine learning": ["machine learning", "ml"],
    "data engineering": ["data engineering", "etl"], "pandas": ["pandas"], "spark": ["apache spark", "pyspark", "spark"],
    "aws": ["aws", "amazon web services"], "docker": ["docker"], "kubernetes": ["kubernetes", "k8s"],
    "tensorflow": ["tensorflow"], "pytorch": ["pytorch"], "power bi": ["power bi", "powerbi"], "tableau": ["tableau"],
}

class SkillExtractor:
    def extract(self, text: str) -> list[str]:
        lowered = text.lower()
        return [canonical for canonical, aliases in SKILL_ALIASES.items()
                if any(re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", lowered) for alias in aliases)]
