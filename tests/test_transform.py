from etl.transform import clean_text, normalize_city, parse_salary
from nlp.skills import SkillExtractor

def test_clean_text_removes_html_and_collapses_whitespace():
    assert clean_text("<p>Python &amp;   SQL</p>") == "Python & SQL"

def test_city_aliases_are_canonical():
    assert normalize_city("Karachi, Pakistan") == "Karachi"

def test_salary_range_is_parsed():
    assert parse_salary("PKR 100,000 - 150,000")["max_amount"] == 150000

def test_skill_aliases_are_normalized():
    assert {"python", "sql"}.issubset(SkillExtractor().extract("Python with MySQL"))
