import os
import json
from flask import render_template, send_from_directory, make_response, request, Response
from src import app, vision, systembolaget


@app.route('/')
@app.route('/result')
@app.route('/result/water')
@app.route('/api')
def basic_pages():
    """ Handles the basic routes for html pages. """
    return make_response(open('src/templates/index.html').read())


@app.route('/api/picture', methods=["POST"])
def picture():
    """
    API endpoint for picture analysis.
    Expects a JSON object in the form {'image': a b64 encoded image}.

    Returns a JSON object with image data acquired from the Google Vision API.
    """
    if request.headers['Content-Type'] == 'application/json':
        imagedata, status = vision.analyse(request.json['image'])
        return Response(imagedata, status=status, mimetype='application/json')
    else:
        app.logger.error('Problem with data, request body looked like this (%s)', request.data)
        return Response("payload needs to be in JSON-format", status=400)


@app.route('/api/beverages', methods=['GET'])
def beverages():
    """
    API endpoint returns a suitable drink depending on query parameters.

    price_score   -- float between 1 and 100 (required).
    alcohol_score -- float between 1 and 100 (required).
    hour  -- integer between 0 and 23 (optional).
             if the value is out range not provided, hour is set to 23.
    month -- integer between 1 and 12 (optional).
             if the value is out range not provided, month is set to 12.

    Returns a JSON object representing a beverage from systemAPI.
    """
    p_score = request.args.get('price_score')
    a_score = request.args.get('alcohol_score')
    hour    = request.args.get('hour')
    month   = request.args.get('month')

    if not (p_score and a_score):
        return Response("Not enough parameters provided", status=400)

    try:
        p_score = float(p_score)
        a_score = float(a_score)
    except ValueError:
        return Response("price_score and alcohol_score must be of type float or integer", status=400)

    if not 1 <= p_score <= 100:
        return Response("price_score must be a value between 1 and 100", status=400)
    if not 1 <= a_score <= 100:
        return Response("alcohol_score must be a value between 1 and 100", status=400)

    if hour is None:
        hour = 23
    if month is None:
        month = 12

    try:
        hour  = int(hour)
        month = int(month)
    except:
        return Response("hour and month must be of type integer", status=400)

    if not 0 <= hour <= 23:
        hour = 23
    if not 1 <= month <= 12:
        month = 12

    params = [p_score, a_score, hour, month]
    beverage_data = systembolaget.get_beverage(params)
    return Response(beverage_data, status=200, mimetype="application/json")


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
