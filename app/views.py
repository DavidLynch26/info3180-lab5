"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os
import datetime
from app import app, db
from app.models import Movie
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from flask import render_template, request, jsonify, send_file, session, send_from_directory

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/movies', methods=['GET', 'POST'])
def movies():
    form = MovieForm()
    if form.validate_on_submit() and request.method == "POST":
        photo = form.poster.data
        title = form.title.data
        created_at = datetime.datetime.now()
        description = form.description.data
        filename = secure_filename(photo.filename)

        photo.save(
            os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename))

        movie = Movie(
            title,
            description,
            filename,
            created_at)

        db.session.add(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": title,
            "poster": filename, 
            "description": description
            })
    elif request.method == "GET":
        movies = db.session.execute(db.select(Movie)).scalars()
        movies = [{'id': movie.id, 'title': movie.title, 'description': movie.description, 'poster': "/api/v1/posters/"+movie.poster} for movie in movies]
        return jsonify({'movies': movies})
    else:
        return jsonify({ 
            "errors": 
                form_errors(form)
            })

@app.route('/api/v1/posters/<filename>')
def get_image(filename):
    print(filename)
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']),filename)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404