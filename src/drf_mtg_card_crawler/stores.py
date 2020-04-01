import requests
from logging import getLogger


logger = getLogger('django')


def luckshack(term):
    results = []
    url = "https://luckshack.co.za/index.php?route=product/product/autocomplete&filter_name={}&version=3".format(term)

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        try:
            res = response.json()['json']
            first = res[0]
        except (KeyError, ValueError) as exc:
            logger.exception(exc)
        except (IndexError):
            pass
        else:
            for r in res:
                url = r.pop("url", None)
                results.append({
                    "url": url,
                    "metadata": r
                })

    return results


def dracoti(term):
    results = []
    url = "https://shop.dracoti.co.za/wc-api/wc_ps_legacy_api/?action=get_result_popup"

    data = {
        "q": term,
        "limit": 8,
        "cat_in": 0,
        "widget_template": "sidebar",
        "row": 7,
        "text_lenght": 100,
        "show_price": 1,
        "show_in_cat": 1,
        "search_in": "%7B%22product%22%3A%226%22%2C%22post%22%3A%220%22%2C%22page%22%3A%220%22%2C%22p_sku%22%3A%220%22%2C%22p_cat%22%3A%220%22%2C%22p_tag%22%3A%220%22%7D"
    }

    response = requests.post(url, data, timeout=5)
    if response.status_code == 200:
        try:
            res = response.json()
            first = res[1]
        except (KeyError, ValueError, IndexError):
            return results
        else:
            # Remove the header element.
            for r in res:
                if r["type"] == "product":
                    url = r.pop("url", None)
                    results.append({
                        "url": url,
                        "metadata": r
                    })

    return results


def topdecksa(term):
    results = []
    url = "https://store.topdecksa.co.za/search?type=product&q=title:*{}*&view=json".format(term)

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        try:
            res = response.json()['results']
            first = res[0]
        except (KeyError, ValueError) as exc:
            logger.exception(exc)
        except (IndexError):
            pass
        else:
            for r in res:
                url = r.pop("url", None)
                results.append({
                    "url": url,
                    "metadata": r
                })

    return results


def sadrobot(term):
    results = []
    url = "https://www.sadrobot.co.za/wp-admin/admin-ajax.php?action=flatsome_ajax_search_products&query={}".format(term)

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        try:
            res = response.json()['suggestions']
            first = res[0]
        except (KeyError, ValueError) as exc:
            logger.exception(exc)
        except (IndexError):
            pass
        else:
            for r in res:
                url = r.pop("url", None)
                results.append({
                    "url": url,
                    "metadata": r
                })

    return results


def hqgaming(term):
    results = []
    url = "https://hqgaming.co.za/search/suggest.json?q={}&resources[type]=product".format(term)

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        try:
            res = response.json()['resources']['results']['products']
            first = res[0]
        except (KeyError, ValueError) as exc:
            logger.exception(exc)
        except (IndexError):
            pass
        else:
            for r in res:
                if r["available"] == True:
                    url = r.pop("url", None)
                    results.append({
                        "url": url,
                        "metadata": r
                    })

    return results


def thewarren(term):
    results = []
    url = "http://www.thewarren.co.za/json/product_search?query={}".format(term)

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    response = requests.get(url, headers=headers, timeout=5)

    if response.status_code == 200:
        try:
            res = response.json()
            first = res[0]
        except (KeyError, ValueError) as exc:
            logger.exception(exc)
        except (IndexError):
            pass
        else:
            for r in res:
                slug = r.get("slug", "")
                url = "http://www.thewarren.co.za/shop/card/{}".format(slug)
                results.append({
                    "url": url,
                    "metadata": r
                })

    return results


def aifest(term):
    results = []
    url = "https://store.ai-fest.co.za/search?q={}&limit=10&timestamp=1585690156863&ajaxSearch=1&id_lang=1".format(term)

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        try:
            res = response.json()
            first = res[0]
        except (KeyError, ValueError) as exc:
            logger.exception(exc)
        except (IndexError):
            pass
        else:
            for r in res:
                url = r.pop("product_link", None)
                results.append({
                    "url": url,
                    "metadata": r
                })

    return results


def battlewizards(term):
    return []


def underworldconnections(term):
    return []
