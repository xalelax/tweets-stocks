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
    """Retrieves full text from extended tweets/retweets"""
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


def search(query, until=None, result_type='popular'):
    """Wrapper for api.search(); returns list of (possibly)
    extended tweets (up to 280 characters).

    Caveat: until must be a datetime object"""

    fmt = '%Y-%m-%d'
    until_formatted = until.strftime(fmt)
    search_result = api.search(query + ' -filter:retweets',
                               until=until_formatted,
                               tweet_mode='extended',
                               result_type=result_type,
                               count=100)
    tweets = [{'created_at': tweet.created_at,
               'author': tweet.user.screen_name,
               'retweet_count': tweet.retweet_count,
               'text': get_full_text(tweet)}
              for tweet in search_result]
    return tweets


def get_tweets(query, min_date, max_date):
    """Twitter's search api returns only 15 results when
    result_type='popular'. Here, I make as many queries
    as needed to get historical data"""

    tweets = search(query, until=max_date)
    if not tweets:
        return []

    dates = [tweet['created_at'] for tweet in tweets]

    calls = 1
    while dates and (min(dates) > min_date) and calls < 4:
        older_tweets = get_tweets(query, min_date, max_date=min(dates))
        dates = [tweet['created_at'] for tweet in older_tweets]
        tweets.extend(older_tweets)

    return tweets
