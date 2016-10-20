# vision.py handels communications with the Google Vision API
import json
import requests
from numpy import interp
from src import app
url = "https://karlroos-systemet.p.mashape.com/product"
# config fil git ignore
key = app.config.get('SYSTEMET_KEY')
headers = {"X-Mashape-Key": key, "Accept": "application/json"}


def get_beverage(imagedata, category):
    payload = map_values(category,
                         imagedata['emotionScore'],
                         imagedata['brightness'],
                         imagedata['ecological'])
    res = requests.get(url, headers=headers, params=payload)
    return res


def map_values(category, emotion_score, brightness, ecological):
    new_dict = {}
    new_dict['tag'] = category['tag']
    '''new_dict['alcohol_from'] = interp(brightness, [1, 100],
                                      [category['alcohol_from'],
                                      category['alcohol_to']])
    new_dict['alcohol_to'] = category['alcohol_to']'''
    '''new_dict['apk_from'] = category['apk_from']
    new_dict['apk_to'] = category['apk_to']'''
    new_dict['price_from'] = interp(emotion_score, [1, 100],
                                    [category['price_from'],
                                     category['price_to']])
    new_dict['price_to'] = category['price_to']
    # new_dict['ecological'] = ecological
    new_dict['order'] = 'ASC'
    new_dict['order_by'] = 'price'
    new_dict["limit"] = 1
    print()
    print("NEW DICT")
    print(new_dict)
    print()
    return new_dict
