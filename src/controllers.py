import os
import json
import base64
from flask import render_template, send_from_directory, make_response, request, Response
from src import app, vision, systembolaget
categories = json.loads(app.config.get('CATEGORIES'))


# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about')
def basic_pages():
    return make_response(open('src/templates/index.html').read())


@app.route('/api')
def api():
    return "INFO ABOUT API AS HTML/TEXT"


@app.route('/api/picture', methods=["POST"])
def picture():
    if request.method == 'POST' and request.is_json:
        imagedata = vision.analyse(request.json['image'])
        return Response(imagedata, status=200, mimetype='application/json')
    else:
        return Response("payload needs to be in JSON-format", status=400)


@app.route('/api/beverages', methods=['GET'])
def beverages():
    if request.method == 'GET':
        # decodes the query param back into a JSON object
        imagedata = json.loads(decode_base64(request.query_string).decode('utf-8'))
        beveragedata = systembolaget.get_beverage(imagedata, categories[5])
        return Response(beveragedata, status=200, mimetype="application/json")
    else:
        return Response("Query must be base64encoded JSON-object", status=400)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.b64decode(data)
