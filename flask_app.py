from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convolution')
def blog_convolution():
    return render_template('convolution.html')

if __name__ == '__main__':
    app.run()
