import os
import json
import base64
from flask import render_template, send_from_directory, make_response, request, Response
from src import app, vision, systembolaget


# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/result')
@app.route('/result/water')
@app.route('/api')
def basic_pages():
    return make_response(open('src/templates/index.html').read())


@app.route('/api/picture', methods=["POST"])
def picture():
    if request.method == 'POST':
        imagedata, status = vision.analyse(request.json['image'])
        return Response(imagedata, status=status, mimetype='application/json')
    else:
        app.logger.error('Problem with data, request body looked like this (%s)', request.data)
        app.logger.info('Error')
        return Response("payload needs to be in JSON-format", status=400)


@app.route('/api/beverages', methods=['GET'])
def beverages():
    if request.method == 'GET':
        p_score = request.args.get('price_score')
        a_score = request.args.get('alcohol_score')
        hour    = request.args.get('hour')
        month   = request.args.get('month')

        if not (p_score and a_score):
            return Response("Not enough parameters provided", status=400)
        if hour is None:
            hour = "23"
        if month is None:
            month = "12"

        params = [p_score, a_score, hour, month]
        beveragedata = systembolaget.get_beverage(params)
        return Response(beveragedata, status=200, mimetype="application/json")


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
