# import os
# import json
# import sys
# import scrapy
# from scrapy.exceptions import CloseSpider
#
# sys.path.append("/app")
# from utils import get_random_user_agent, format_user_input
#
# BRAND = format_user_input(sys.argv[3])
# CATEGORY = format_user_input(sys.argv[5])
# SOURCE = format_user_input(sys.argv[7])
# PRODUCT_URLS = format_user_input(sys.argv[9])
# AMOUNT = int(format_user_input(sys.argv[11]))
# IMAGES = format_user_input(sys.argv[13])
# # IMAGES = int(format_user_input(sys.argv[13]))
#
# PROXY = "http://lum-customer-truum2-zone-unblocker-country-fr:zao08gx2mfcc@zproxy.lum-superproxy.io:22225"
# PRODUCT_XPATH = "//div[contains(@class, 'list__container')]//article[contains(@class, 'product-thumbnail')]//a[contains(@class, 'product-thumbnail__details-wrapper') and not(contains(@href, 'css'))]/@href"
# NEXT_PAGE_XPATH = "//span[contains(@class, 'next')]//parent::a//@href"
#
# DOWNLOADED_URLS = []
#
# urls_checker = {}
#
# if PRODUCT_XPATH is None:
#     raise Exception("Product xpath not configured!")
#
# if BRAND and CATEGORY and IMAGES == "n":
#     with open(f"/app/brands/{BRAND}/config.json", "r") as input_file:
#         CONFIG = json.loads(input_file.read())
#
#     if not os.path.isdir(f"/html_files/{BRAND}"):
#         os.mkdir(f"/html_files/{BRAND}")
#     if not os.path.isdir(f"/html_files/{BRAND}/{CATEGORY}"):
#         os.mkdir(f"/html_files/{BRAND}/{CATEGORY}")
#
#
# class DownloaderSpider(scrapy.Spider):
#     name = "downloader"
#     start_urls = CONFIG.get("listing_page").get(CATEGORY)
#     urls_list = []
#     product_urls = []
#     counter_page_limit = 0
#     counter_next_page = 1
#     item_number = 0
#
#     # def start_requests(self):
#     #     once_list = [
#     #         "https://www.auchan.fr/azgenon-siege-gaming-z50-noir/pr-C1683862",
#     #         "https://www.auchan.fr/sumup-kit-terminal-de-paiement-socle-station-de-recharge-blanc/pr-C1491963",
#     #         "https://www.auchan.fr/tp-link-point-d-acces-sans-fil-tl-wa865re/pr-C644542",
#     #         "https://www.auchan.fr/skross-adaptateur-world-to-euro-blanc/pr-C1767216",
#     #         "https://www.auchan.fr/sumup-terminal-de-paiement-solo-avec-socle-de-recharge/pr-C1535158",
#     #         "https://www.auchan.fr/beko-cuisiniere-a-gaz-fsg62010fw-60cm-4-foyers-four-a-gaz/pr-C1606171",
#     #         "https://www.auchan.fr/selecline-cuisiniere-a-gaz-600146818-4-foyers-four-a-gaz/pr-C1730541",
#     #         "https://www.auchan.fr/haier-table-induction-aspirante-haih6iescf/pr-4ac2f875-67ab-428b-979e-01f7f8632d16",
#     #         "https://www.auchan.fr/bosch-refrigerateur-combine-kgn36vled-serie-4-vitafresh/pr-305a4550-c535-45f6-afb0-fd4a4f611870",
#     #         "https://www.auchan.fr/lg-lave-linge-hublot-f82av35whs/pr-85014d7d-945a-469d-90f6-0deaee992907"
#     #     ]
#     #     for item in once_list:
#     #         absolute_url = item
#     #         if absolute_url not in DOWNLOADED_URLS:
#     #             DOWNLOADED_URLS.append(absolute_url)
#     #             yield scrapy.Request(
#     #                 url=absolute_url,
#     #                 callback=self.parse_html,
#     #                 headers={"User-Agent": get_random_user_agent()},
#     #                 # meta={"proxy": PROXY},
#     #             )
#
#     # if SOURCE == "y":
#     #     start_urls = [CONFIG.get("product_urls").get(CATEGORY)][0]
#     # else:
#     #     start_urls = [CONFIG.get("listing_page").get(CATEGORY)]
#
#     def start_requests(self):
#         if SOURCE == "y":
#             for url in self.start_urls:
#                 if url not in DOWNLOADED_URLS:
#                     DOWNLOADED_URLS.append(url)
#                     yield scrapy.Request(
#                         url=url,
#                         callback=self.parse,
#                         # callback=self.parse_html,
#                         headers={"User-Agent": get_random_user_agent()},
#                         # meta={"proxy": PROXY},
#                     )
#         else:
#             counter = 0
#             for url in self.start_urls:
#                 print(f"\n\n\n\n\n{counter}: {url}\n\n\n\n\n")
#                 counter += 1
#                 yield scrapy.Request(
#                     url=url,
#                     callback=self.parse,
#                     headers={"User-Agent": get_random_user_agent()},
#                     # meta={"proxy": PROXY},
#                 )
#         # else:
#         #     for urls in self.start_urls:
#         #         for url in urls:
#         #             yield scrapy.Request(
#         #                 url=url,
#         #                 callback=self.parse,
#         #                 headers={"User-Agent": get_random_user_agent()},
#         #                 # meta={"proxy": PROXY},
#         #             )
#
#     def parse(self, response):
#         items = response.xpath(PRODUCT_XPATH).getall()
#         base_url = response.url.split("?")[0]
#         if not urls_checker.get(base_url):
#             urls_checker[base_url] = {}
#
#         urls_checker[response.url] = {"total number": len(items)}
#         for i in items:
#             urls_checker[response.url].update({f"https://www.auchan.fr{i}": 0})
#         with open(f"/app/brands/{BRAND}/urls_unchecked.json", "w") as checker:
#             checker.write(json.dumps(urls_checker, indent=4))
#
#         print("Total items:", len(items))
#
#         if len(items) > 0:
#
#             for item in items:
#                 absolute_url = response.urljoin(item)
#                 if absolute_url not in DOWNLOADED_URLS:
#                     DOWNLOADED_URLS.append(absolute_url)
#                     yield scrapy.Request(
#                         url=absolute_url,
#                         callback=self.parse_html,
#                         headers={"User-Agent": get_random_user_agent()},
#                         # meta={"proxy": PROXY},
#                     )
#
#                 # if PRODUCT_URLS == "y" and AMOUNT:
#                 #     if len(self.product_urls) < AMOUNT:
#                 #         self.product_urls.append(absolute_url)
#                 #     if len(self.product_urls) == AMOUNT:
#                 #         CONFIG["product_urls"][CATEGORY] = self.product_urls
#                 #         with open(f"/app/brands/{BRAND}/config.json", "w") as output_file:
#                 #             output_file.write(json.dumps(CONFIG, indent=4))
#                 #
#                 # if absolute_url not in self.urls_list:
#                 #     self.urls_list.append(absolute_url)
#                 #     yield scrapy.Request(
#                 #         url=absolute_url,
#                 #         callback=self.parse_html,
#                 #         headers={"User-Agent": get_random_user_agent()},
#                 #         # meta={"proxy": PROXY},
#                 #     )
#
#         if NEXT_PAGE_XPATH:
#             next_page = response.urljoin(response.xpath(NEXT_PAGE_XPATH).get())
#             items = response.xpath(PRODUCT_XPATH).getall()
#             # else:
#             #     self.counter_next_page += 1
#             #     next_page = f"{self.start_urls[0]}?page={self.counter_next_page}"
#             #     items = response.xpath(PRODUCT_XPATH).getall()
#
#             if next_page and len(items) > 0:
#                 yield scrapy.Request(
#                     url=next_page,
#                     callback=self.parse,
#                     headers={"User-Agent": get_random_user_agent()},
#                     # meta={"proxy": PROXY},
#                 )
#
#     def parse_html(self, response):
#         if AMOUNT and self.counter_page_limit >= AMOUNT:
#             raise CloseSpider("You have reached the limit :)")
#         self.counter_page_limit += 1
#         self.item_number += 1
#         filename = f'{self.item_number}-{response.url.split("/")[-1] + ".html"}'
#         file_path = f"/html_files/{BRAND}/{CATEGORY}/{filename}"
#         with open(file_path, "wb") as file:
#             file.write(response.body)
