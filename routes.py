"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convolution')
def blog_convolution():
    return render_template('convolution.html')

@app.route('/publications')
def publications():
    return render_template('publications.html')

@app.route('/about')
def about():
    return render_template('about.html')
