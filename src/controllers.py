import os
import json
import base64
from flask import render_template, send_from_directory, make_response, request, Response
from src import app, vision, systembolaget


# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/result')
@app.route('/result/water')
@app.route('/about')
def basic_pages():
    return make_response(open('src/templates/index.html').read())


@app.route('/api')
def api():
    return "INFO ABOUT API AS HTML/TEXT"


@app.route('/api/picture', methods=["POST"])
def picture():
    if request.method == 'POST' and request.is_json:
        imagedata, status = vision.analyse(request.json['image'])
        return Response(imagedata, status=status, mimetype='application/json')
    else:
        app.logger.error('Problem with data, request body looked like this (%s)', request.data)
        app.logger.info('Error')
        return Response("payload needs to be in JSON-format", status=400)


@app.route('/api/beverages', methods=['GET'])
def beverages():
    if request.method == 'GET':
        price   = request.args.get('price')
        alcohol = request.args.get('alcohol')
        eco     = request.args.get('ecological')
        hour    = request.args.get('hour')
        month   = request.args.get('month')

        if not (price and alcohol and eco and hour and month):
            return Response("Not enough parameters provided", status=400)

        params = [price, alcohol, eco, hour, month]
        beveragedata, status = systembolaget.get_beverage(params)
        return Response(beveragedata, status=status, mimetype="application/json")
    else:
        return Response("Query must be base64encoded JSON-object", status=400)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
