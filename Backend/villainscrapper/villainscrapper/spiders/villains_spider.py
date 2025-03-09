import scrapy
from scrapy_playwright.page import PageMethod
from urllib.parse import urljoin
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class VillainsSpider(scrapy.Spider):
    name = "villains"
    allowed_domains = ["villains.fandom.com"]
    start_urls = ["https://villains.fandom.com/wiki/Category:Movie_Villains"]

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": False},  # Change to False for debugging
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "CONCURRENT_REQUESTS": 5,
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".category-page__members-wrapper", timeout=10000),
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    ],
                },
                callback=self.parse
            )

    def parse(self, response):
        self.logger.info(f"Scraping URL: {response.url}")

        # Save response for debugging
        with open("scrapy_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        # Extract villain links
        villains = response.css(".category-page__members-wrapper a::attr(href)").getall()
        if not villains:
            self.logger.warning("No villains found. Check selectors.")

        for villain in villains:
            full_url = urljoin(response.url, villain)
            yield {"name": villain.split("/")[-1].replace("_", " "), "url": full_url}

        # Handle pagination
        next_page = response.css('.category-page__pagination-next::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Next Page: {next_page_url}")

            yield scrapy.Request(
                next_page_url, 
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".category-page__members-wrapper", timeout=10000),
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    ],
                },
                callback=self.parse
            )
