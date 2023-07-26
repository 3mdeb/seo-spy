#!/usr/bin/env python3

import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.orphan_pages_spider import OrphanPagesSpider

STATUS_OK = 0
STATUS_ERR = 1
STATUS_FAILURE = 2


class SeoSpy():
    def parse_program_input(self):
        """
        Parse program input parameters.

        Parameters:
            self (object): The instance of the class containing this method.

        Returns:
            Parser args (object): An object that contains the parsed arguments
                                  extracted from the program input.
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

    def check_connection(self, crawler):
        """
        Checks if the crawler has visited any page.

        Parameters:
            self (object): The instance of the class containing this method.
            crawler (object): The network crawler object responsible for
                              handling the connection.

        Returns:
            int:
                - 0 (STATUS_OK): If some pages were visited by the crawler.
                - 1 (STATUS_ERR): If no pages were visited by the crawler.
        """
        connection_issue = crawler.stats.get_value("custom/connection_issue")

        if connection_issue:
            print("================================================")
            print("Connection Issue.")
            print("================================================")
            print("No sites visited. Check the connection to the domain.")
            return STATUS_ERR
        else:
            return STATUS_OK

    def orphan_pages(self, domain):
        """
        Find orphan pages on the given domain.

        Parameters:
            self (object): The instance of the class containing this method.
            domain (str): The domain name to be scanned for orphan pages.

        Returns:
            int:
                - 0 (STATUS_OK): If no orphan pages were found on the domain.
                - 1 (STATUS_ERR): If there was a connection issue.
                - 2 (STATUS_FAILURE): If orphan pages were found on the domain.
        """
        status: int
        settings = get_project_settings()
        process = CrawlerProcess(settings=settings)
        process.crawl(OrphanPagesSpider, domain=domain)
        crawler = list(process.crawlers)[0]
        process.start()

        status = self.check_connection(crawler)
        if status is not STATUS_OK:
            return STATUS_ERR

        orphan_pages = crawler.stats.get_value("custom/orphan_pages")
        if orphan_pages:
            print("================================================")
            print("Orphan pages found:")
            print("================================================")
            for page in orphan_pages:
                print(page)
            return STATUS_FAILURE
        else:
            print("================================================")
            print("Orphan pages not found.")
            print("================================================")
            return STATUS_OK


def main():
    """
    Entry point of the SEO Spy application.

    Parameters:
        None

    Returns:
        int:
            - 0 (STATUS_OK): If the application completes successfully.
            - 1 (STATUS_ERR): If there was a internal error
                              (eg. connection issue)
            - 2 (STATUS_FAILURE): If SEO tasks failed (eg. orphan pages were
                                  found or some pages do not have canonical
                                  meta tag)
    """
    status: int

    spy = SeoSpy()
    args = spy.parse_program_input()
    if args.orphan:
        status = spy.orphan_pages(args.domain)
        exit(status)
    else:
        spy.parser.print_help()
    exit(0)


if __name__ == "__main__":
    main()
