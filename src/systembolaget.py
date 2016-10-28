"""systembolaget.py handels the communication with systemetAPI"""
import json
import requests
import random
from numpy import interp
from datetime import datetime
from src import app


categories       = json.loads(app.config.get('CATEGORIES'))
categories_times = json.loads(app.config.get('CATEGORIES_TIMES'))

url     = "https://karlroos-systemet.p.mashape.com/product"
key     = app.config.get('SYSTEMET_KEY')
headers = {"X-Mashape-Key": key, "Accept": "application/json"}


def get_beverage(params):
    """
    Requests a beverag by aplying the params to a base category and turning it
    into a request systemetAPI can handle.

    Keyword Arguments:
    params -- list containing price score, alcohol score, eco, hour, month

    Returns a result from systemetAPI
    """

    p_score = float(params[0])
    a_score = float(params[1])
    hour    = int(params[2])
    month   = int(params[3])

    category = _get_category(hour, month)

    payload = _map_values(category, price, alcohol)

    res = requests.get(url, headers=headers, params=payload)
    return res, 200



def _map_values(category, p_score, a_score):
    """
    Maps the parameters to values in the category

    Keyword Arguments:
    category -- Category to map other parameters to.
    p_score -- the value to map to category['price_from']
    a_score -- the value to map to category['alcohol_from']

    Returns a new dictionary.
    """
    new_dict = {}
    new_dict['tag'] = category['tag']
    new_dict['alcohol_from'] = ('% 6.2f' % interp(a_score, [1, 100],
                                                  [category['alcohol_from'],
                                                  category['alcohol_to']]))
    new_dict['alcohol_to'] = category['alcohol_to']
    new_dict['price_from'] = ('% 6.2f' % interp(p_score, [1, 100],
                                                [category['price_from'],
                                                category['price_to']]))
    new_dict['price_to'] = category['price_to']
    new_dict['order'] = 'ASC'
    new_dict['order_by'] = 'price'
    new_dict["limit"] = 1

    print(new_dict)
    return new_dict


def _get_category(hour, month):
    """
    Returns one of several possible categories depending on the hour of the day
    and month of the year.

    Keyword Arguments:
    hour -- integer representing hour of day.
    month -- intger representing month of the year.

    Returns a category
    """
    possible_categories = categories_times[str(hour)]
    if month == 12:
        xmas_category = categories_times["xmas"]
        possible_categories.append(xmas_category)
    random_choice = str(random.choice(possible_categories))
    category = categories[random_choice]
    return category
