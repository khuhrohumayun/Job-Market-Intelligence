"""Robots and explicit-approval gate for responsible collection."""
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import requests
from config.settings import settings

class SourceNotApprovedError(PermissionError):
    pass

def assert_collection_allowed(url: str, approved: bool) -> None:
    """Fail closed unless a human has approved the source's terms and purpose."""
    if not approved:
        raise SourceNotApprovedError("Source is not approved. Review its terms, privacy policy, and robots.txt first.")
    parsed = urlparse(url)
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
    parser = RobotFileParser(robots_url)
    try:
        response = requests.get(robots_url, timeout=settings.request_timeout_seconds, headers={"User-Agent": settings.user_agent})
        if response.ok:
            parser.parse(response.text.splitlines())
            if not parser.can_fetch(settings.user_agent, url):
                raise SourceNotApprovedError(f"robots.txt disallows collection: {url}")
    except requests.RequestException as exc:
        raise SourceNotApprovedError(f"Could not verify robots.txt: {exc}") from exc
