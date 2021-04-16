import requests
from logging import getLogger

from bs4 import BeautifulSoup
from django.utils.timezone import now


logger = getLogger('django')


CONNECTION_ERROR = "Unexpected error connecting to the store."
RESPONSE_CODE_ERROR = "Unexpected response code from the store."
RESPONSE_FORMAT_ERROR = "Unexpected response format from the store."


def luckshack(term):
    error = None
    results = []
    url = "https://luckshack.co.za/index.php?route=product/product/autocomplete&filter_name={}&version=3".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    try:
        res = response.json()['json']
        first = res[0]
    except IndexError:
        pass
    except Exception as exc:
        logger.exception(exc)
        error = RESPONSE_FORMAT_ERROR
    else:
        for r in res:
            url = r.pop("url", None)
            name = r.pop("name", None)
            image = r.pop("image", None)
            results.append({
                "url": url,
                "name": name,
                "image": image,
                "metadata": r
            })

    return results, error


def dracoti(term):
    error = None
    results = []
    url = "https://shop.dracoti.co.za/wc-api/wc_ps_legacy_api/?action=get_result_popup"

    data = {
        "q": term,
        "limit": 10,
        "cat_in": 0,
        "widget_template": "sidebar",
        "row": 7,
        "text_lenght": 100,
        "show_price": 1,
        "show_in_cat": 1,
        "search_in": "%7B%22product%22%3A%226%22%2C%22post%22%3A%220%22%2C%22page%22%3A%220%22%2C%22p_sku%22%3A%220%22%2C%22p_cat%22%3A%220%22%2C%22p_tag%22%3A%220%22%7D"
    }

    try:
        response = requests.post(url, data, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    try:
        res = response.json()
        first = res[1]
    except IndexError:
        pass
    else:
        # Remove the header element.
        for r in res:
            if r["type"] == "product":
                url = r.pop("url", None)
                name = r.pop("title", None)
                image = r.pop("image_url", None)
                results.append({
                    "url": url,
                    "name": name,
                    "image": image,
                    "metadata": r
                })

    return results, error


def topdecksa(term):
    """
    Top Deck

    System: Shopify
    """

    error = None
    results = []
    url = "https://store.topdecksa.co.za/search/suggest.json?q={}&resources[type]=product&resources[limit]=10&resources[options][unavailable_products]=hide&resources[options][fields]=title,product_type,variants.title,vendor".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    try:
        res = response.json()["resources"]["results"]["products"]
        first = res[0]
    except IndexError:
        pass
    except Exception as exc:
        logger.exception(exc)
        error = RESPONSE_FORMAT_ERROR
    else:
        for r in res:
            url = r.pop("url", None)
            name = r.pop("title", None)
            image = r.pop("image", None)
            results.append({
                "url": f"https://store.topdecksa.co.za{url}",
                "name": name,
                "image": image,
                "metadata": r
            })

    return results, error


def sadrobot(term):
    error = None
    results = []
    url = "https://www.sadrobot.co.za/wp-admin/admin-ajax.php?action=flatsome_ajax_search_products&query={}".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    try:
        res = response.json()['suggestions']
        first = res[0]
    except IndexError:
        pass
    except Exception as exc:
        logger.exception(exc)
        error = RESPONSE_FORMAT_ERROR
    else:
        for r in res:
            url = r.pop("url", None)
            name = r.pop("value", None)
            image = r.pop("img", None)
            results.append({
                "url": url,
                "name": name,
                "image": image,
                "metadata": r
            })

    return results, error


def hqgaming(term):
    """
    DEPRECATED: This store is no longer operating.
    """

    raise Exception("Not supported!")

    error = None
    results = []
    url = "https://hqgaming.co.za/search/suggest.json?q={}&resources[type]=product".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    try:
        res = response.json()['resources']['results']['products']
        first = res[0]
    except IndexError:
        pass
    except Exception as exc:
        logger.exception(exc)
        error = RESPONSE_FORMAT_ERROR
    else:
        for r in res:
            if r["available"] == True:
                url = r.pop("url", None)
                results.append({
                    "url": url,
                    "metadata": r
                })

    return results, error


def thewarren(term):
    error = None
    results = []
    url = "http://www.thewarren.co.za/json/product_search?query={}".format(term)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    try:
        res = response.json()
        first = res[0]
    except IndexError:
        pass
    except Exception as exc:
        logger.exception(exc)
        error = RESPONSE_FORMAT_ERROR
    else:
        for r in res:
            slug = r.pop("slug", None)
            url = "http://www.thewarren.co.za/shop/card/{}".format(slug)
            name = r.pop("name", None)
            results.append({
                "url": url,
                "name": name,
                "image": "https://via.placeholder.com/150.jpg",
                "metadata": r
            })

    return results, error


def aifest(term):
    error = None
    results = []
    url = "https://store.ai-fest.co.za/search?q={}&limit=10&timestamp={}&ajaxSearch=1&id_lang=1".format(term, now().timestamp())

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    try:
        res = response.json()
        first = res[0]
    except IndexError:
        pass
    except Exception as exc:
        logger.exception(exc)
        error = RESPONSE_FORMAT_ERROR
    else:
        for r in res:
            url = r.pop("product_link", None)
            results.append({
                "url": url,
                "metadata": r
            })

    return results, error


def battlewizards(term):
    error = None
    results = []
    url = "http://www.battlewizards.co.za/search.php?search_query={}&section=product".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.findAll("li", class_="product")

    for product in products[:10]:
        image = product.article.figure.a.div.img
        title_box = product.findAll("h4", class_="card-title")
        price_box = product.findAll("span", class_="price--withTax")

        data = {
            "url": title_box[0].a.get("href"),
            "name": title_box[0].a.string,
            "image": image.get("data-src"),
            "metadata": {
                "price": price_box[0].string
            }
        }
        results.append(data)

    return results, error


def underworldconnections(term):
    error = None
    results = []
    url = "https://underworldconnections.com/?s={}&shop_load=search&post_type=product&shop_filters_layout=header".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.findAll("li", class_="product")

    for product in products:
        image = product.div.a.img
        title_box = product.findAll("h3")
        price_box = product.findAll(
            "span", class_="woocommerce-Price-amount"
        )

        data = {
            "url": title_box[0].a.get("href"),
            "name": title_box[0].a.string,
            "image": image.get("data-src"),
            "metadata": {
                "price": price_box[0].find(text=True, recursive=False)
            }
        }
        results.append(data)

    return results, error
