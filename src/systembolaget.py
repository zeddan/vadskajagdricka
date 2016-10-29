"""systembolaget.py handels the communication with systemetAPI"""
import json
import requests
import random
from numpy import interp
from datetime import datetime
from src import app


CATEGORIES       = json.loads(app.config.get('CATEGORIES'))
CATEGORIES_TIMES = json.loads(app.config.get('CATEGORIES_TIMES'))

URL     = "https://karlroos-systemet.p.mashape.com/product"
KEY     = app.config.get('SYSTEMET_KEY')
HEADERS = {"X-Mashape-Key": KEY, "Accept": "application/json"}


def get_beverage(params):
    """
    Requests a beverage by applying the params to a base category and turning it
    into a request systemetAPI can handle.

    Keyword Arguments:
    params -- list containing price score, alcohol score, hour, month.

    Returns a Response object.
    """
    p_score = float(params[0])
    a_score = float(params[1])
    hour    = int(params[2])
    month   = int(params[3])

    category = _get_category(hour, month)
    payload = _map_values(category, p_score, a_score)
    res = requests.get(URL, headers=HEADERS, params=payload)
    return res


def _map_values(category, p_score, a_score):
    """
    Maps the parameters to values in the category.

    Keyword Arguments:
    category -- the category to map other parameters to.
    p_score -- the value to map to category['price_from'].
    a_score -- the value to map to category['alcohol_from'].

    Returns a dictionary containing the new values.
    """
    new_dict = {}
    a_mapped = interp(a_score, [1, 100], [category['alcohol_from'], category['alcohol_to']])
    p_mapped = interp(p_score, [1, 100], [category['price_from'], category['price_to']])
    new_dict['price_from'] = '%0.2f' % p_mapped
    new_dict['price_to'] = category['price_to']
    new_dict['alcohol_from'] = '%0.2f' % a_mapped
    new_dict['alcohol_to'] = category['alcohol_to']
    new_dict['tag'] = category['tag']
    new_dict['order'] = 'ASC'
    new_dict['order_by'] = 'price'
    new_dict["limit"] = 1
    return new_dict


def _get_category(hour, month):
    """
    Returns one of several possible categories depending on the hour of the day
    and month of the year.

    Keyword Arguments:
    hour -- integer representing hour of day.
    month -- integer representing month of the year.

    Returns a category.
    """
    possible_categories = CATEGORIES_TIMES[str(hour)]
    if month == 12:
        xmas_category = CATEGORIES_TIMES["xmas"]
        possible_categories.append(xmas_category)
    random_choice = str(random.choice(possible_categories))
    category = CATEGORIES[random_choice]
    return category
