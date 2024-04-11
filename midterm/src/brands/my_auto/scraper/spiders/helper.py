import re
import sys
import json

sys.path.append("/app")

def prettify_text(text):
    text = "".join(text)
    return (
        re.sub(r"\s+", " ", text)
            .strip()
            .replace("\r", "")
            .replace("\n", "")
            .replace("\t", "")
            .strip()
    )

def get_key_value_data(response):
    key_value_data = {}

    # key_value data
    key_value_xpath = "//div[@class='detail-row d-flex align-items-center font-size-13 px-sm-24px px-16px py-8px']"
    try:
        key_value_xpath = response.xpath(key_value_xpath)
        for i in key_value_xpath:
            product_key = prettify_text(i.xpath(".//div[@class='w-50 w-md-40 text-gray-850']//text()").getall())
            values_xpath = i.xpath(".//div[@class='w-50 w-md-60 text-gray-800']//text()").getall()
            values = []
            for value in values_xpath:
                item = prettify_text(value)
                if item and item not in values:
                    values.append(item)
            if product_key and values:
                if key_value_data.get(product_key):
                    key_value_data.get(product_key).get("values").append("".join(values[0]))
                elif not key_value_data.get(product_key):
                    key_value_data.update({product_key: "".join(values)})

    except Exception:
        pass

    # price
    price_xpath = "//div[@class='d-flex align-items-center']//p//text()"
    try:
        price = response.xpath(price_xpath).get()
        price = price.replace(",", "").replace(" $","")
        if price:
            key_value_data.update({"Price": f"{price}$"})
    except Exception:
        pass

    key_value_data.pop("Exchange")
    return key_value_data
