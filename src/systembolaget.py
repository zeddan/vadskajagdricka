# vision.py handels communications with the Google Vision API
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



def get_beverage(imagedata):
    date = datetime.now()
    hour = date.hour
    month = date.month

    if 9 <= hour <= 12:
        return {"No drinks are available during 09:00 - 12:00"}, 204

    category = get_category(hour, month)
    payload = map_values(category,
                         imagedata['emotionScore'],
                         imagedata['brightness'],
                         imagedata['ecological'])
    res = requests.get(url, headers=headers, params=payload)
    return res, 200



def map_values(category, emotion_score, brightness, ecological):
    new_dict = {}
    new_dict['tag'] = category['tag']
    new_dict['alcohol_from'] = interp(brightness, [1, 100],
                                      [category['alcohol_from'],
                                      category['alcohol_to']])
    new_dict['alcohol_to'] = category['alcohol_to']
    new_dict['price_from'] = interp(emotion_score, [1, 100],
                                    [category['price_from'],
                                     category['price_to']])
    new_dict['price_to'] = category['price_to']
    new_dict['ecological'] = ecological
    new_dict['order'] = 'ASC'
    new_dict['order_by'] = 'price'
    new_dict["limit"] = 1
    return new_dict

def get_category(hour, month):
    possible_categories = categories_times[str(hour)]
    if month == 12:
        xmas_category = categories_times["xmas"]
        possible_categories.append(xmas_category)
    random_choice = str(random.choice(possible_categories))
    category = categories[random_choice]
    return category
