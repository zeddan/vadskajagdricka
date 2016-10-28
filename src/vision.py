"""vision.py handels communications with the Google Vision API"""
import requests
import json
from numpy import interp
from src import app

url = 'https://vision.googleapis.com/v1/images:annotate?fields=responses&key='
key = app.config.get('VISION_KEY')
emotion_matrix = json.loads(app.config.get('EMOTION_MATRIX'))
emotion_value = {'VERY_UNLIKELY': 1, 'UNLIKELY': 2, 'POSSIBLE': 3, 'LIKELY': 4, 'VERY_LIKELY': 5}


def analyse(byte_string_image):
    """
    Takes a string as input. This should be a base64encoded representation of
    an image.

    Keyword Arguments:
    byte_string_image -- string

    Returns a filterd response from google vision API as a JSON-object.
    """

    imageRequest = {
        "requests": [
            {
               "image": {
                "content": byte_string_image
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
               "imageContext": {
               }
              }
             ]
            }

    response = requests.post(url+key, json=imageRequest).json()

    if 'faceAnnotations' and 'labelAnnotations' not in response['responses'][0]:
            return {}, 422
    else:
        result = _filter(response)
        return json.dumps(result), 200


def _filter(response):
    """
    Filters a response from the Vision API and returns a new dictionary with
    emotionScore, brightness, labels and ecological values.

    Keyword Arguments:
    response -- dictionary

    Returns a new dictionary.
    """
    new_dict = {}
    res = response['responses'][0]
    emotions = {}
    colors = []
    labels = []
    face = res['faceAnnotations'][0]
    emotions['joy'] = face['joyLikelihood']
    emotions['surprise'] = face['surpriseLikelihood']
    emotions['headwear'] = face['headwearLikelihood']
    emotions['sorrow'] = face['sorrowLikelihood']
    emotions['anger'] = face['angerLikelihood']
    new_dict['emotionScore'] = _calculate_score(emotions, face['detectionConfidence'])

    for color in res['imagePropertiesAnnotation']['dominantColors']['colors']:
        colors.append(color['color'])
    new_dict['brightness'] = _calculate_brightness(colors)
    print("brightness: " + str(new_dict['brightness']))

    labels.append(res['labelAnnotations'][0]['description'])
    labels.append(res['labelAnnotations'][1]['description'])
    new_dict['labels'] = labels

    print(new_dict['emotionScore'])
    print(new_dict['labels'])
    return new_dict


def _calculate_score(emotions, confidence):
    print(emotions)
    """
    Calulates an emotion score amd returns the highest score.
    Calculation is done by mapping the emotion value to a number between 0.04-1.0
    and multiplying it with the detectionConfidence.

    Keyword Arguments:
    emotions -- a list with emotions from the Vision API response.
    confindce -- detectionConfidence from the Vision API response.

    Returns highest score.
    """
    emotion = ""
    higest_value = -1
    for k, v in emotions.items():
        print(k, v)
        value = emotion_value[v]
        if value > higest_value:
            higest_value = value
            emotion = k

    score = confidence * emotion_matrix[emotion][emotions[emotion]]
    print(score)
    return score * 100


def _calculate_brightness(colors):
    """
    Sums all values in the colors list and maps that to a value between 1-100.

    Keyword Arguments:
    colors -- a list of all the colors from the Vision API response.

    Returns value between 1-100
    """
    max_value = (255 * 3) * len(colors)
    brightness = 0
    for color in colors:
        r = int(color['red'])
        g = int(color['green'])
        b = int(color['blue'])
        brightness += r + b + g
    br = interp(brightness, [0, max_value], [1, 100])
    return br
