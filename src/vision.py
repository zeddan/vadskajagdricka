"""vision.py handels communications with the Google Vision API"""
import requests
import json
from numpy import interp
from src import app

URL = 'https://vision.googleapis.com/v1/images:annotate?fields=responses&key='
KEY = app.config.get('VISION_KEY')

EMOTION_MATRIX = json.loads(app.config.get('EMOTION_MATRIX'))
EMOTION_VALUES = {
    'VERY_UNLIKELY': 1,
    'UNLIKELY':      2,
    'POSSIBLE':      3,
    'LIKELY':        4,
    'VERY_LIKELY':   5
}


def analyse(img_b64):
    """
    Takes a base64 encoded string as input.
    Packages it in a Vision API request friendly format.

    Keyword Arguments:
    img_b64 -- base64 encoded string

    Returns a filterd response from the Vision API as a JSON object.
    """
    image_request = {
      "requests": [
        {
          "image": {
            "content": img_b64
          },
          "features": [
            {
              "type": "FACE_DETECTION",
              "maxResults": 1
            },
            {
              "type": "LABEL_DETECTION",
              "maxResults": 2
            },
            {
              "type": "IMAGE_PROPERTIES",
              "maxResults": 1
            }
          ],
          "imageContext": {}
        }
      ]
    }
    response = requests.post(URL+KEY, json=image_request).json()
    r = response['responses'][0]
    if not {'faceAnnotations', 'labelAnnotations'} <= set(r):
        return {}, 422
    else:
        result = _filter(response)
        return json.dumps(result), 200


def _filter(response):
    """
    Filters the response from the Vision API and returns a new dictionary with
    emotion_score, color_score and labels values.

    Keyword Arguments:
    response -- dictionary containing the response to filter.
    """
    new_dict = {}
    emotions = {}
    color = {}
    labels = []
    res = response['responses'][0]
    face = res['faceAnnotations'][0]
    emotions['joy'] = face['joyLikelihood']
    emotions['surprise'] = face['surpriseLikelihood']
    emotions['headwear'] = face['headwearLikelihood']
    emotions['sorrow'] = face['sorrowLikelihood']
    emotions['anger'] = face['angerLikelihood']
    new_dict['emotion_score'] = _calc_emotion_score(emotions, face['detectionConfidence'])

    color = res['imagePropertiesAnnotation']['dominantColors']['colors'][0]['color']
    new_dict['color_score'] = _calc_color_score(color)

    labels.append(res['labelAnnotations'][0]['description'])
    labels.append(res['labelAnnotations'][1]['description'])
    new_dict['labels'] = labels
    return new_dict


def _calc_emotion_score(emotions, confidence):
    """
    Finds the highest emotion value and calculates a score based on
    the values in the emotion values matrix and the confidence.

    Keyword Arguments:
    emotions -- a list with emotions from the Vision API response.
    confindce -- detectionConfidence from the Vision API response.

    Returns integer number between 1 and 100.
    """
    emotion = ""
    higest_value = -1
    for k, v in emotions.items():
        value = EMOTION_VALUES[v]
        if value > higest_value:
            higest_value = value
            emotion = k
    score = confidence * EMOTION_MATRIX[emotion][emotions[emotion]]
    return score * 100


def _calc_color_score(color):
    """
    Sums rgb values and maps to a value between 1-100.

    Keyword Arguments:
    color -- dict with the dominant color from the Vision API response.

    Returns integer number between 1 and 100.
    """
    max_value = (255 * 3)
    color_sum = 0
    r = int(color['red'])
    g = int(color['green'])
    b = int(color['blue'])
    color_sum = r + g + b
    color_score = interp(color_sum, [0, max_value], [1, 100])
    return color_score
