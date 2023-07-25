from scrapy.spiders import SitemapSpider
from urllib.parse import urljoin


class OrphanPagesSpider(SitemapSpider):
    name = "orphan_pages_spider"
    allowed_domains = ["127.0.0.1"]
    sitemap_urls = ["http://127.0.0.1:8000/sitemap.xml"]
    _visited_pages: list = []
    _incoming_links: list = []

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
        Parse list of links internal and create list of urls based on sitemap.
        """
        hrefs = response.xpath("//a/@href").getall()
        self._visited_pages.append(response.url)

        for link in hrefs:
            incoming_link: str = link
            base_link = response.url
            if (
                incoming_link.startswith("https://") or
                incoming_link.startswith("http://") or
                incoming_link.startswith("#")
            ):
                continue
            while(incoming_link.startswith("..")):
                link_rel = base_link.split("/")[-2] + "/"
                base_link = base_link.split(link_rel)[0]
                incoming_link = incoming_link[2:]
                if incoming_link:
                    incoming_link = incoming_link[1:]

            incoming_link = urljoin(base_link, incoming_link)
            incoming_link = incoming_link.split("#")[0]
            if incoming_link not in self._incoming_links:
                self._incoming_links.append(incoming_link)

    def closed(self, reason):
        """
        Verify whether each URL possesses incoming internal links.
        In case it lacks such links, include it in the list of orphan pages.
        """
        orphan_pages = []
        for url in self._visited_pages:
            if not url.endswith("/"):
                url = url + "/"
            if url not in self._incoming_links:
                orphan_pages.append(url)
        if not orphan_pages:
            self.logger.info("No orphan pages found.")
        else:
            self.logger.error("Orphan pages found:")
            for orphan_page in orphan_pages:
                self.logger.error(f"{orphan_page}")
                self.crawler.stats.set_value(
                    "custom/orphan_pages",
                    orphan_pages
                )
