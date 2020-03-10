import tweepy
from dotenv import load_dotenv
import os
load_dotenv()

consumer_key = os.environ['API_KEY']
consumer_secret = os.environ['API_SECRET_KEY']
access_token = os.environ['TW_ACCESS_TOKEN']
access_token_secret = os.environ['TW_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
