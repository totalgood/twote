import tweepy
from . import secrets


def get_api():
    auth = tweepy.OAuthHandler(secrets.TEST_CONSUMER_KEY, secrets.TEST_CONSUMER_SECRET)
    auth.set_access_token(secrets.TEST_ACCESS_TOKEN, secrets.TEST_ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def tweepy_send_tweet(tweet):
    api = get_api()
    print("api: {}".format(api))
    status = api.update_status(status=tweet)
    print("status result: {}".format(status))
    return None
