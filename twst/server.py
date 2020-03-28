import stockdata
import twitter
from flask import Flask, render_template, jsonify
app = Flask(__name__)


@app.route('/')
def main(name=None):
    return render_template('main.html', name=name)


@app.route('/data/<symbol>/<word>')
def get_data(symbol, word):  # TODO : refactor this function
    candles = stockdata.get_candles(str(symbol))
    tweets = twitter.search(str(word))
    # Giving back only time and opening_prices
    stock_data = {'t': candles['t'], 'o': candles['o']}

    return jsonify({'stock_data': stock_data,
                    'tweets': tweets})
