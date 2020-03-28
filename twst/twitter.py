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


def get_full_text(status):
    if hasattr(status, "retweeted_status"):  # Check if Retweet
        try:
            return 'RT ' + status.retweeted_status.full_text
        except AttributeError:
            return 'RT ' + status.retweeted_status.text
    else:
        try:
            return status.full_text
        except AttributeError:
            return status.text


def search(query, result_type='popular'):
    """Wrapper for api.search(); returns list of (possibly)
    extended tweets (up to 280 characters)"""
    search_result = api.search(query + ' -filter:retweets',
                               tweet_mode='extended',
                               result_type=result_type,
                               count=100)
    tweets = [{'created_at': tweet.created_at,
               'author': tweet.user.screen_name,
               'retweet_count': tweet.retweet_count,
               'text': get_full_text(tweet)}
              for tweet in search_result]
    return tweets
