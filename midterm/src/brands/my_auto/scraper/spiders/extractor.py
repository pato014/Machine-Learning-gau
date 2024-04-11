import os
import sys

import scrapy
from .helper import get_key_value_data
sys.path.append("/app")

def format_user_input(input):
    return input.split("=")[-1]


BRAND = format_user_input(sys.argv[3])
CATEGORY = format_user_input(sys.argv[5])

sys.path.append(f"/app/brands/{BRAND}/scraper/spiders")

FILTER_ID = []


class ExtractorSpider(scrapy.Spider):
    name = "extractor"
    limit = 0
    single_mode = False

    if single_mode:
        filename = None
        start_urls = [f"file:///html_files/{BRAND}/product_pages/{CATEGORY}/{filename}"]
    else:
        start_urls = [f"file:///html_files/{BRAND}/product_pages/{CATEGORY}/{{}}"]

    def start_requests(self):
        urls = self.start_urls
        files_path = [f"/html_files/{BRAND}/product_pages/{CATEGORY}/"]

        for path in files_path:
            if self.limit:
                files = os.listdir(path)[: self.limit]
            else:
                files = os.listdir(path)

            for index, file in enumerate(files):
                url = urls[0].format(file)
                yield scrapy.Request(url, callback=self.parse, meta={"file": file})

    def parse(self, response):
        yield get_key_value_data(response)
