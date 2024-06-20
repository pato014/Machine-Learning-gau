import os
import scrapy
import sys
import json
import argparse

sys.path.append("/app")
from utils import get_formatted_date, format_user_input

parser = argparse.ArgumentParser(description="receives command-line arguments")
parser.add_argument("--brand", type=str, help="Brand name")
parser.add_argument("--category", type=str, help="Category name")

args = parser.parse_known_args(sys.argv[-1].split(" "))[0]
BRAND = args.brand
if not BRAND:
    BRAND = format_user_input(sys.argv[3])
CATEGORY = args.category
if not CATEGORY:
    CATEGORY = format_user_input(sys.argv[5])

sys.path.append(f"/app/brands/{BRAND}/truum_scraper/spiders")
import helper

checker = []
duplicates = []
invalid_ids = {}


class ExtractorSpider(scrapy.Spider):
    name = "extractor"
    limit = 0
    single_mode = False

    if single_mode:
        filename = None
        start_urls = [f"file:///html_files/{BRAND}/{CATEGORY}/{filename}"]
    else:
        start_urls = [f"file:///html_files/{BRAND}/{CATEGORY}/{{}}"]

    def start_requests(self):
        urls = self.start_urls
        files_path = [f"/html_files/{BRAND}/{CATEGORY}/"]

        for path in files_path:
            if self.limit:
                files = os.listdir(path)[: self.limit]
            else:
                files = os.listdir(path)

            for index, file in enumerate(files):
                url = urls[0].format(file)
                yield scrapy.Request(url, callback=self.parse, meta={"file": file})

    def parse(self, response):

        print(f"\n\n\n\n\n\n\n\n{len(checker)}\n\n\n\n\n\n\n\n{len(duplicates)}")
        if helper.get_id(response) == "N/A" or not helper.get_id(response).isdigit():
            invalid_ids.update({helper.get_url(response): helper.get_id(response)})

        with open("invalid_ids.jsonl", "w") as file:
            content = json.dumps(invalid_ids)
            file.write(content)

        product_id = helper.get_id(response)
        # if product_id not in checker:
        #     checker.append(product_id)
        yield {
            "id": helper.get_id(response),
            "name": helper.get_name(response),
            "timestamp": get_formatted_date(),
            "brand": helper.get_brand(response),
            "url": helper.get_url(response),
            "listing_url": helper.get_listing_url(response),
            "breadcrumbs": helper.get_breadcrumbs(response),
            "category": helper.get_category(response).title(),
            "out_of_stock_display_text": helper.get_stock(response),
            "sellers": helper.get_sellers(response),
            "keyValueData": helper.get_key_value_data(response),
            "freeText": [],
            "images": helper.get_images(response),
            # "url": helper.get_url(response),
            # "file": response.meta.get("file")
        }
        # else:
        #     duplicates.append(product_id)
        #     print("_________________________________________________", "Duplicate omited!")
        #     print(len(duplicates))
