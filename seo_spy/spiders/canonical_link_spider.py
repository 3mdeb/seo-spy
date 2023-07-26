from scrapy.spiders import SitemapSpider
from urllib.parse import urljoin


class CanonicalLinkSpider(SitemapSpider):
    name = "canonical_link_spider"
    allowed_domains = ["127.0.0.1"]
    sitemap_urls = ["http://127.0.0.1:8000/sitemap.xml"]
    _visited_pages: list = []
    _pages_with_no_canonical: list = []

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        if "domain" in self.__dict__:
            if not (
                self.__dict__["domain"].startswith("https://") or
                self.__dict__["domain"].startswith("http://")
            ):
                raise ValueError(
                    "Domain URL must start with https:// or http://"
                )
            domain = self.__dict__["domain"]
            allowed_domain = domain.split("//")[-1].split(":")[0]
            self.allowed_domains = [allowed_domain]
            self.sitemap_urls = [urljoin(domain, "sitemap.xml")]

    def parse(self, response):
        """
        Create list of urls based on sitemap.
        """
        self._visited_pages.append(response.url)
        canonical = response.xpath('//link[@rel="canonical"]')
        self.logger.info(f"Canonical: {canonical}")
        if not canonical:
            self._pages_with_no_canonical.append(response.url)

    def closed(self, reason):
        """
        Verify whether each URL possesses incoming internal links.
        In case it lacks such links, include it in the list of orphan pages.
        """
        if not self._visited_pages:
            self.logger.error(
                "No sites visited. Check the connection to the domain."
            )
            self.crawler.stats.set_value(
                "custom/connection_issue",
                True
            )
            return
        if not self._pages_with_no_canonical:
            self.logger.info("Every page has canonical link.")
        else:
            self.logger.error("Pages with no canonical link found:")
            for page in self._pages_with_no_canonical:
                self.logger.error(f"{page}")
                self.crawler.stats.set_value(
                    "custom/canonical",
                    self._pages_with_no_canonical
                )
