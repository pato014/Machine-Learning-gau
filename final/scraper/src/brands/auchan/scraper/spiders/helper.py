import re
import sys

sys.path.append("/app")
from utils import prettify_text, get_element_by_xpath, get_format


def get_id(response):
    result = "N/A"
    product_description = prettify_text(response.xpath("//span[contains(text(), 'EAN')]//following-sibling::div//text()").getall())
    if product_description:
        result = product_description.split("/")[-1].strip()
    return result


def get_name(response):
    element_xpath = "//h1//text()"
    return get_element_by_xpath(response, element_xpath, multiple=True, prettify=True)


def get_brand(response):
    element_xpath = "//meta[contains(@itemprop, 'brand')]//@content"
    return get_element_by_xpath(response, element_xpath, multiple=False, prettify=False)


def get_url(response):
    element_xpath = "//link[contains(@rel, 'canonical')]/@href"
    return get_element_by_xpath(response, element_xpath, multiple=False, prettify=False)


def get_listing_url(response):
    element_xpath = "//div[contains(@class, 'site-breadcrumb__wrapper')]//span//a//@href"
    result = f"https://www.auchan.fr{response.xpath(element_xpath).getall()[-2]}"
    return result


def get_breadcrumbs(response):
    result = []
    element_xpath = "//div[contains(@class, 'site-breadcrumb__wrapper')]//span//text()"
    try:
        breadcrumbs_list = response.xpath(element_xpath).getall()
        result.append({"format": "texts", "values": "/".join(i.strip() for i in breadcrumbs_list[1:-1])})
    except Exception:
        pass
    return result


def get_category(response):
    breadcrumbs = response.xpath("//div[contains(@class, 'site-breadcrumb__wrapper')]//span//text()").getall()
    if len(breadcrumbs) > 0:
        return breadcrumbs[-2]
    else:
        return "N/A"


def get_stock(response):  # 15136005 check
    element_xpath = ""
    return get_element_by_xpath(response, element_xpath, multiple=True, prettify=True)


def get_sellers(response):
    seller = response.xpath("//span[contains(@class, 'offer-selector__marketplace-label')]//span//text()").get()
    if not seller:
        seller = response.xpath("//a[contains(@class, 'offer-selector__marketplace-label-underline')]//text()").get()
        # seller = prettify_text(
        #     response.xpath("//a[contains(@class, 'offer-selector__marketplace-label-underline')]//text()").get())
    element_xpath = "//meta[contains(@itemprop, 'price')]//@content"
    try:
        price = response.xpath(element_xpath).get()
        if price:
            return {"format": "texts", "values": {seller: {"amount": str(price), "currency": "EUR"}}}
    except Exception:
        pass
    return {"format": "texts", "values": {"N/A": {"amount": "N/A", "currency": "N/A"}}}


def get_key_value_data(response):
    key_value_dict = {}

    # Libellé web principal
    try:
        principal_xpath = "//div[contains(@class, 'offer-selector__description-header')]/following-sibling::div//text()"
        principal = response.xpath(principal_xpath).getall()
        if principal:
            key_value_dict.update({"Libellé web principal": get_format("text", principal)})
    except Exception:
        pass

    # Eco-Part
    try:
        eco_list = response.xpath("//section[contains(@class, 'offer-selector__price-container')]")
        unfiltered_eco = []
        for i in eco_list:
            item = prettify_text(i.xpath(".//ul[contains(@class, 'offer-selector__taxes')]//text()").getall())
            if item:
                unfiltered_eco.append(item)
        eco = []
        for i in unfiltered_eco:
            if i not in eco:
                eco.append(i)
        eco = [i.replace("dont", "").strip() for i in eco]  # TODO: check eco part
        if eco[0]:
            key_value_dict.update({"Eco-Part": get_format("text", eco)})
    except Exception:
        pass

    # warranty
    try:
        warranty_xpath = "//p[contains(@itemprop, 'warranty')]//text()"
        warranty = response.xpath("//p[contains(@itemprop, 'warranty')]//text()").get().replace("Garantie fabricant: ",
                                                                                                "")
        if warranty:
            warranty = [warranty]
            key_value_dict.update({"Garantie Fabricant": get_format("text", warranty)})
    except Exception:
        pass

    # pictograms
    try:
        pictogram_xpath = "//div[contains(@class, 'product-legals__infos-item')]"
        pictograms = response.xpath(pictogram_xpath)
        for i in pictograms:
            key = prettify_text(i.xpath("./span//text()").getall())
            value = i.xpath(".//img//@alt").get().replace(" /10", "")
            if key and value:
                value = [value]
                key_value_dict.update({f"{key} pictogram": get_format("text", value)})
    except Exception:
        pass

    # description
    try:
        description = []
        description_xpath = "//div[contains(@id, 'product-description-only')]//text()"
        description_list = response.xpath(description_xpath).getall()
        for i in description_list:
            item = prettify_text(i)
            if item and item != "Description":
                description.append(item)
        if description:
            key_value_dict.update({"Description": get_format("text", description)})
    except Exception:
        pass

    # characteristics
    characteristics_xpath = response.xpath(
        "//div[contains(@id, 'product-features')]//div[contains(@class, 'product-description__feature-wrapper')]")
    characteristics_names = []

    for i in characteristics_xpath:
        name = prettify_text(i.xpath(".//h3//text()").getall())
        if not name:
            key = prettify_text(i.xpath(".//h5//text()").getall())
            value = prettify_text(i.xpath(".//div[contains(@class, 'single')]//span//text()").getall())
            if key and value:
                value = [value]
                key_value_dict.update({key: get_format("text", value)})
        if name:
            characteristics_names.append(name)
        key_value_xpath = i.xpath(".//div[contains(@class, 'product-description__feature-group-wrapper')]")
        for j in key_value_xpath:
            key = prettify_text(j.xpath(".//span[contains(@class, 'label')]//text()").getall())
            value = prettify_text(j.xpath(".//span[contains(@class, 'value')]//text()").getall())
            if not value and "Réf / EAN :" in key:
                key = "Réf / EAN"
                value = prettify_text(
                    response.xpath("//span[contains(text(), 'Réf / EAN :')]//parent::div//div//text()").getall())
            if key and value:
                value = [value]
                key_value_dict.update({key: get_format("text", value)})

    try:
        regulatory_xpath = response.xpath(
            "//div[contains(@class, 'product-legals__block')]//div[contains(@class, 'product-legals__download-item')]//a")
        for i in regulatory_xpath:
            key = prettify_text(i.xpath(".//text()").getall())
            value = [i.xpath(".//@href").get()]
            key_value_dict.update({key: get_format("document", value)})
    except Exception:
        pass

    # images desciption
    try:
        images_description = []
        try:
            images_description = response.xpath(
                "//div[contains(@class, 'product-zoom__items galleryScroller')]//img//@alt").getall()
        except Exception:
            pass
        key_value_dict.update({"Images Description": get_format("text", images_description)})
    except Exception:
        pass

    result = []
    if key_value_dict:
        result.append({"name": "Product Details", "values": key_value_dict})
    return result


def get_images(response):
    result = []
    images = []
    try:
        first_image = [
            response.xpath("//div[contains(@class, 'product-zoom__item galleryItem selected')]//img//@src").get()]
        other_images = response.xpath(
            "//div[contains(@class, 'product-zoom__items galleryScroller')]//img//@data-src").getall()
        if first_image[0] or other_images[0]:
            images = first_image + other_images
    except Exception:
        pass
    result.append(get_format("images", images))
    return result
