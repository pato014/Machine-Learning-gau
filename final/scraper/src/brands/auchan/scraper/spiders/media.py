# import os
# import scrapy
# import json
# import sys
#
# sys.path.append("/app")
# from utils import format_user_input
#
# BRAND_NAME = format_user_input(sys.argv[3])
# CATEGORY_NAME = format_user_input(sys.argv[5])
# IMAGES = format_user_input(sys.argv[7])
#
# REPARABILITY = "Télécharger l’indice de réparabilité"
# ENERGY = "Télécharger la classe énergétique"
# EURODOC = "Télécharger la fiche européenne"
#
# if IMAGES == "y":
#     main_dict = {}
#
#     with open(f"{CATEGORY_NAME}.jsonl", "r") as file:
#         my_file = file.readlines()
#         for i in my_file:
#             json_data = json.loads(i)
#             product_id = json_data.get("id")
#             images = json_data.get("images")[0].get("values")
#             documents = []
#
#             if REPARABILITY in str(json_data):
#                 reparability = \
#                     json_data.get("keyValueData")[0].get("values").get(REPARABILITY).get(
#                         "values")[0]
#                 documents.append({"reparability": reparability})
#             if ENERGY in str(json_data):
#                 energy = json_data.get("keyValueData")[0].get("values").get(ENERGY).get(
#                     "values")[0]
#                 documents.append({"energy": energy})
#             if EURODOC in str(json_data):
#                 eurodoc = json_data.get("keyValueData")[0].get("values").get(EURODOC).get(
#                     "values")[0]
#                 documents.append({"eurodoc": eurodoc})
#
#             main_dict.update({product_id: {"images": images, "documents": documents}})
#
#     for product_id in main_dict:
#         if not os.path.isdir(f"/html_files/{BRAND_NAME}/media/{CATEGORY_NAME}/{product_id}/documents"):
#             os.makedirs(f"/html_files/{BRAND_NAME}/media/{CATEGORY_NAME}/{product_id}/documents", exist_ok=True)
#
#
#     class MediaSpider(scrapy.Spider):
#         name = "media"
#
#         def start_requests(self):
#             for product_id, product_urls in main_dict.items():
#                 images = product_urls.get("images")
#                 for url in images:
#                     if "static" not in url:
#                         yield scrapy.Request(url=url, callback=self.parse_images, meta={"id": product_id})
#                 documents = product_urls.get("documents")
#                 for item in documents:
#                     for name, url in item.items():
#                         yield scrapy.Request(url=url, callback=self.parse_documents,
#                                              meta={"id": product_id, "name": name})
#
#         def parse_images(self, response):
#             path = f"/html_files/{BRAND_NAME}/media/{CATEGORY_NAME}/{response.meta.get('id')}/"
#             # filename = response.url.replace("https://media.auchan.fr/", "").split("_")[0]
#             filename = (len(os.listdir(path)) - 1) + 1
#             with open(f"{path}/{filename}", 'wb') as html_file:
#                 html_file.write(response.body)
#
#         # def parse_documents(self, response):
#         #     path = f"/html_files/{BRAND_NAME}/media/{CATEGORY_NAME}/{response.meta.get('id')}/documents"
#         #     filename = response.meta.get('name')
#         #     with open(f"{path}/{filename}", 'wb') as html_file:
#         #         html_file.write(response.body)
