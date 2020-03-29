from finnhub import client as Finnhub
from os import environ

client = Finnhub.Client(api_key=environ['FH_API_KEY'])


def get_candles(symbol, resolution='D', count=12):
    response = client.stock_candle(symbol=symbol,
                                   resolution=resolution,
                                   count=count)
    return response
