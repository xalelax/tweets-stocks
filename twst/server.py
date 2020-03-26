from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def main(name=None):
    return render_template('main.html', name=name)
