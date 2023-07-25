#!/usr/bin/env python3

import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.orphan_pages_spider import OrphanPagesSpider


class SeoSpy():
    def gather_parameters(self):
        """
        Parse program input parameters.
        """
        self.parser = argparse.ArgumentParser(
            description=(
                "SEO Spy is a Python-based web scraping tool that functions as"
                " an SEO error checking tool, leveraging the capabilities of "
                "the renowned web scraper Scrapy."
            )
        )
        self.parser.add_argument(
            "-d",
            "--domain",
            required=True,
            help=(
                "URL of the tested domain. Examples: "
                "http://127.0.0.1:8000 https://docs.dasharo.com"
            )
        )
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-o",
            "--orphan",
            action="store_true",
            help="Run orphan pages check"
        )

        return self.parser.parse_args()

    def orphan_pages(self, domain):
        settings = get_project_settings()
        process = CrawlerProcess(settings=settings)
        process.crawl(OrphanPagesSpider, domain=domain)
        crawler = list(process.crawlers)[0]
        process.start()

        orphan_pages = crawler.stats.get_value("custom/orphan_pages")
        if orphan_pages:
            print("================================================")
            print("Orphan pages found:")
            print("================================================")
            for page in orphan_pages:
                print(page)
            exit(1)
        else:
            print("================================================")
            print("Orphan pages not found.")
            print("================================================")


def main():
    spy = SeoSpy()
    args = spy.gather_parameters()
    if args.orphan:
        spy.orphan_pages(args.domain)
    else:
        spy.parser.print_help()
    exit(0)


if __name__ == "__main__":
    main()
