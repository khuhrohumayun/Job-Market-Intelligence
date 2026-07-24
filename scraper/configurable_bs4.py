"""Configuration-driven BeautifulSoup scraper for approved static listing pages."""
from dataclasses import dataclass
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from scraper.base import BaseScraper
from scraper.contracts import RawJobPosting
from scraper.policy import assert_collection_allowed

@dataclass(frozen=True)
class SelectorConfig:
    source_name: str
    start_url: str
    approved: bool
    card: str
    title: str
    company: str
    link: str
    source_id_attribute: str = "data-job-id"
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    posted: str | None = None
    next_page: str | None = None

class ConfigurableBeautifulSoupScraper(BaseScraper):
    def __init__(self, config: SelectorConfig) -> None:
        self.config = config
        self.source_name = config.source_name
        super().__init__()

    @staticmethod
    def _text(card, selector: str | None) -> str | None:
        element = card.select_one(selector) if selector else None
        return element.get_text(" ", strip=True) if element else None

    def parse(self, html: str, page_url: str):
        soup = BeautifulSoup(html, "html.parser")
        for index, card in enumerate(soup.select(self.config.card), start=1):
            link = card.select_one(self.config.link)
            if link is None or not link.get("href"):
                self.logger.warning("Skipping card without link on %s", page_url)
                continue
            source_id = card.get(self.config.source_id_attribute) or f"{page_url}#{index}"
            title, company = self._text(card, self.config.title), self._text(card, self.config.company)
            if not title or not company:
                self.logger.warning("Skipping incomplete card %s", source_id)
                continue
            yield RawJobPosting(source=self.source_name, source_job_id=source_id, url=urljoin(page_url, link["href"]),
                title=title, company=company, description=self._text(card, self.config.description),
                location=self._text(card, self.config.location), salary_text=self._text(card, self.config.salary),
                posted_text=self._text(card, self.config.posted)).to_dict()

    def clean(self, raw_record: dict) -> dict:
        return raw_record

    def next_page(self, html: str, page_url: str) -> str | None:
        if not self.config.next_page: return None
        node = BeautifulSoup(html, "html.parser").select_one(self.config.next_page)
        return urljoin(page_url, node["href"]) if node and node.get("href") else None

    def crawl_approved(self, sink, max_pages: int = 1) -> int:
        assert_collection_allowed(self.config.start_url, self.config.approved)
        return self.crawl(self.config.start_url, sink, max_pages=max_pages)
