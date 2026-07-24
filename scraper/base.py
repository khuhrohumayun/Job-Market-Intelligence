"""Extensible, polite scraping contract. Implement adapters only for permitted sources."""
from abc import ABC, abstractmethod
from dataclasses import asdict
import time
from typing import Iterable, Iterator
import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from app.logging import get_logger
from config.settings import settings

class BaseScraper(ABC):
    source_name: str

    def __init__(self) -> None:
        self.logger = get_logger(f"scraper.{self.source_name}")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": settings.user_agent})

    @retry(retry=retry_if_exception_type(requests.RequestException), stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def fetch(self, url: str) -> str:
        """Fetch a permitted public page. Never bypass access controls."""
        response = self.session.get(url, timeout=settings.request_timeout_seconds)
        response.raise_for_status()
        time.sleep(settings.scraper_delay_seconds)
        return response.text

    @abstractmethod
    def parse(self, html: str, page_url: str) -> Iterable[dict]: ...

    @abstractmethod
    def clean(self, raw_record: dict) -> dict: ...

    def save(self, records: Iterable[dict], sink) -> int:
        count = 0
        for record in records:
            sink.write(self.clean(record))
            count += 1
        self.logger.info("Saved %s records", count)
        return count

    def crawl(self, start_url: str, sink, max_pages: int = 1) -> int:
        """Crawl a bounded sequence; subclasses decide how pagination is discovered."""
        saved, url = 0, start_url
        for _ in range(max_pages):
            if not url:
                break
            html = self.fetch(url)
            saved += self.save(self.parse(html, url), sink)
            url = self.next_page(html, url)
        return saved

    def next_page(self, html: str, page_url: str) -> str | None:
        return None
