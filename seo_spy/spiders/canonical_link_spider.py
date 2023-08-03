from scrapy import Spider, Request
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


class CanonicalLinkSpiderNoSitemap(Spider):
    name = "canonical_link_spider_nositemap"
    _visited_pages: list = []
    _incoming_links: list = []
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
            self.domain = self.__dict__["domain"]
            allowed_domain = self.domain.split("//")[-1].split(":")[0]
            self.allowed_domains = [allowed_domain]
            self.start_urls = [self.domain]

    def parse(self, response):
        """
        Create list of urls based on sitemap.
        """
        self._visited_pages.append(response.url)
        canonical = response.xpath('//link[@rel="canonical"]')
        self.logger.info(f"Canonical: {canonical}")
        if not canonical:
            self._pages_with_no_canonical.append(response.url)

        hrefs = response.xpath("//a/@href").getall()

        for link in hrefs:
            incoming_link: str = link
            base_link = response.url
            if (
                incoming_link.startswith("https://") or
                incoming_link.startswith("http://") or
                incoming_link.startswith("mailto:") or
                incoming_link.startswith("#")
            ) and not incoming_link.startswith(self.domain):
                continue
            while(incoming_link.startswith("..")):
                link_rel = base_link.split("/")[-2] + "/"
                base_link = base_link.split(link_rel)[0]
                incoming_link = incoming_link[2:]
                if incoming_link:
                    incoming_link = incoming_link[1:]

            if(incoming_link.startswith("/")):
                base_link = self.domain
                incoming_link = incoming_link[1:]

            incoming_link = urljoin(base_link, incoming_link)
            incoming_link = incoming_link.split("#")[0]
            if not incoming_link.endswith("/"):
                incoming_link = incoming_link + "/"
            if incoming_link not in self._incoming_links:
                self._incoming_links.append(incoming_link)
                yield Request(incoming_link, callback=self.parse)

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
