"""Template adapter. Replace selectors only after confirming a source permits collection."""
from bs4 import BeautifulSoup
from scraper.base import BaseScraper

class ExamplePortalScraper(BaseScraper):
    source_name = "example_portal"
    def parse(self, html: str, page_url: str):
        soup = BeautifulSoup(html, "html.parser")
        for card in soup.select("article.job-card"):
            link = card.select_one("a.job-link")
            yield {"source": self.source_name, "source_job_id": card.get("data-job-id"), "url": link.get("href", page_url) if link else page_url,
                   "title": card.select_one("h2").get_text(" ", strip=True), "company": card.select_one(".company").get_text(" ", strip=True),
                   "description": card.select_one(".description").get_text(" ", strip=True) if card.select_one(".description") else ""}
    def clean(self, raw_record: dict) -> dict:
        return raw_record
