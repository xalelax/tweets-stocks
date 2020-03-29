import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

import twst.stockdata as stockdata
import twst.twitter as twitter

from flask import Flask, render_template, jsonify
from datetime import datetime

# Initialize sentry
sentry_sdk.init(
    dsn="https://8ec0db70183c464d928b08998836c084@sentry.io/5178828",
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)


@app.route('/')
def main(name=None):
    return render_template('main.html', name=name)


@app.route('/data/<symbol>/<word>')
def get_data(symbol, word):  # TODO : refactor this function
    # Getting data from external APIs
    candles = stockdata.get_candles(str(symbol))
    # Return error if no data found
    if 't' not in candles:
        return jsonify({'error': 'Invalid stock symbol'})
    # Converting unix time to datetime for stocks
    stock_data = candles.copy()
    stock_data['t'] = [datetime.fromtimestamp(epoch)
                       for epoch in stock_data['t']]

    # Searching for tweets in overlapping range
    max_date, min_date = max(stock_data['t']), min(stock_data['t'])

    tweets = twitter.get_tweets(str(word), min_date, max_date)

    return jsonify({'stock_data': stock_data,
                    'tweets': tweets})
