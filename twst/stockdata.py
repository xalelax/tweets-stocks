from finnhub import client as Finnhub
from os import environ

client = Finnhub.Client(api_key=environ['FH_API_KEY'])


def get_candles(symbol, resolution=60, count=168):
    response = client.stock_candle(symbol=symbol,
                                   resolution=resolution,
                                   count=count)
    return response
