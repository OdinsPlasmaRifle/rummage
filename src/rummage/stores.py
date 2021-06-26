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
    url = "https://luckshack.co.za/index.php?route=product/asearch&search={}".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.findAll("div", class_="product-thumb")

    for product in products:
        image = product.div.a.img
        title_box = product.findAll("div", class_="caption")[0]
        price = title_box.findAll('td')[1].h5.b

        data = {
            "url": title_box.h4.a.get("href"),
            "name": title_box.h4.a.string.strip(),
            "image": image.get("src"),
            "price": price.string.strip(),
        }
        results.append(data)

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

                # Extract the price from the HTML value in `price`.
                soup = BeautifulSoup(r["price"], 'html.parser')
                price = soup.span.bdi

                results.append({
                    "url": url,
                    "name": name,
                    "image": image,
                    "price": price.text.strip()
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
            price = r.pop("price", None)
            results.append({
                "url": f"https://store.topdecksa.co.za{url}",
                "name": name,
                "image": image,
                "price": price
            })

    return results, error


def sadrobot(term):
    error = None
    results = []
    url = "https://www.sadrobot.co.za/?product_cat=&s={}&post_type=product".format(term)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return results, CONNECTION_ERROR

    if response.status_code != 200:
        return results, RESPONSE_CODE_ERROR

    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.findAll("div", class_="product")

    for product in products:
        # Check if out of stock and skip if out of stock.
        # NOTE : It would be better if we could do this via the GET filters.
        add_cart_button = product.find("div", class_="add-to-cart-button")
        if add_cart_button.a.string.strip() != "Add to cart":
            continue

        image = product.find("div", class_="box-image").div.a.img
        title_box = product.find("p", class_="product-title")
        price = product.find("span", class_="price").span.bdi

        data = {
            "url": title_box.a.get("href"),
            "name": title_box.a.string.strip(),
            "image": image.get("data-src"),
            "price": price.text.strip(),
        }
        results.append(data)

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
                    "url": url
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
                "image": "https://via.placeholder.com/150.jpg"
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
                "url": url
            })

    return results, error


def battlewizards(term):
    error = None
    results = []
    url = "http://www.battlewizards.co.za/search.php?mode=1&search_query_adv={}&brand=&searchsubs=ON&price_from=&price_to=&featured=&shipping=&category%5B%5D=18&category%5B%5D=24&section=product".format(term)

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
            "name": title_box[0].a.string.strip(),
            "image": image.get("data-src"),
            "price": price_box[0].string.strip()
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
            "name": title_box[0].a.string.strip(),
            "image": image.get("data-src"),
            "price": price_box[0].find(text=True, recursive=False)
        }
        results.append(data)

    return results, error
