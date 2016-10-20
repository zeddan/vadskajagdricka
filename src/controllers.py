import os

from flask import render_template, send_from_directory, make_response

from src import app


# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about')
def basic_pages():
    return make_response(open('src/templates/index.html').read())


# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
