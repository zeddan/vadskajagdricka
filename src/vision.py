# vision.py handels communications with the Google Vision API
import requests
import json
from src import app

url = 'https://vision.googleapis.com/v1/images:annotate?fields=responses&key='
key = app.config.get('VISION_KEY')
emotion_matrix = json.loads(app.config.get('EMOTION_MATRIX'))


# takes a base64encode string represting an image
# returns filterd response from google vision API
def analyse(byte_string_image):
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
                 "maxResults": 1
                },
                {
                 "type": "IMAGE_PROPERTIES",
                 "maxResults": 1
                },
                {
                 "type": "SAFE_SEARCH_DETECTION",
                 "maxResults": 1
                }
               ],
               "imageContext": {
               }
              }
             ]
            }
    response = requests.post(url+key, json=imageRequest).json()
    if 'faceAnnotations' not in response['responses'][0]:
            return {}, 422
    else:
        result = filter(response)
        return json.dumps(result), 200


# takes a response as input parameter returns new dictionary
def filter(response):
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
    new_dict['emotionScore'] = calculate_score(emotions, face['detectionConfidence'])

    for color in res['imagePropertiesAnnotation']['dominantColors']['colors']:
        colors.append(color['color'])
        new_dict['brightness'] = calculate_brightness(colors)

    labels.append(res['labelAnnotations'][0]['description'])
    new_dict['labels'] = labels
    if res['safeSearchAnnotation']['adult'] == "VERY_UNLIKELY":
        new_dict['ecological'] = "false"
    else:
        new_dict['ecological'] = "true"
    return new_dict


# takes emotions and confidence as input and returns a score between 1 and 100
def calculate_score(emotions, confidence):
    oldscore = -1
    for x in emotions:
            score = confidence * emotion_matrix[x][emotions[x]]
            if oldscore < score:
                oldscore = score
    return oldscore * 100


# takes colors as input and returns the sum
def calculate_brightness(colors):
    brightness = 0
    for color in colors:
        r = int(color['red'])
        g = int(color['green'])
        b = int(color['blue'])
        brightness += r + b + g
    return brightness/1000
