import twst.twitter as t
import twst.stockdata as s
from twst.server import app, get_data

import pytest
from datetime import datetime, timedelta


@pytest.fixture(scope='module')
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [('authorization', 'DUMMY')],
        "filter_query_parameters": [('token', 'DUMMY')]
    }


@pytest.mark.vcr()
def test_search():
    """Check that tweets have expected attributes"""
    tweets = t.search('physics')
    attributes = ['created_at', 'author', 'retweet_count', 'text']
    for att in attributes:
        for tweet in tweets:
            assert att in tweet
    assert type(tweet['retweet_count']) is int


@pytest.mark.vcr()
def test_search2():
    """Check until argument is working"""
    threshold = datetime.now() - timedelta(days=3)
    tweets = t.search('quantum', threshold)
    for tweet in tweets:
        assert tweet['created_at'] < threshold


@pytest.mark.vcr()
def test_get_candles():
    """Check Finnhub data"""
    data = s.get_candles('AAPL')
    assert data['s'] == 'ok'


@pytest.mark.vcr()
def test_get_data():
    """Check that error is thrown for invalid symbols"""
    with app.app_context():
        data = get_data('Angioi incorporated GmbH', 'Pavarutti')
        assert 'error' in data.json
