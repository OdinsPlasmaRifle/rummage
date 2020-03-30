import requests


def luckshack(term):
    method = "GET"
    url = "https://luckshack.co.za/index.php?route=product/product/autocomplete&filter_name={}&version=3".format(term)

    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        try:
            message = response.json()['json'][0]
        except (KeyError, ValueError, IndexError):
            return False
    else:
        raise Exception("Non-200 response.")

    return True
