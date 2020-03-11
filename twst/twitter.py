import tweepy
import os

# Getting environment variables
consumer_key = os.environ['TW_API_KEY']
consumer_secret = os.environ['TW_API_SECRET_KEY']
access_token = os.environ['TW_ACCESS_TOKEN']
access_token_secret = os.environ['TW_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def search(query):
    """Wrapper for api.search(); returns list of (possibly)
    extended tweets (up to 280 characters)"""
    search_result = api.search(query, tweet_mode='extended')
    tweets = [tweet.full_text for tweet in search_result]
    return tweets
