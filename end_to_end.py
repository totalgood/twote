import django
from django.forms.models import model_to_dict
import sys
import time
import tweepy
import os

# need to point Django at the right settings to access pieces of app
os.environ["DJANGO_SETTINGS_MODULE"] = "hackor.settings"
django.setup()

from twote.models import OutgoingConfig
from twote.serializers import TweetSerializer
from twote.secrets import listener, sender 


class TwitterBot:
    """
    Class that helps run the actions in an end to end test of the twitter bot.
    """
    def __init__(self, account):
        # tw_api is access point to all Tweepy methods
        self.tw_api = self.setup_tw_api(account)
        self.user_info = self.get_user_info()

    def setup_tw_api(self, account):
        auth = tweepy.OAuthHandler(account["CONSUMER_KEY"], account["CONSUMER_SECRET"])
        auth.set_access_token(account["ACCESS_TOKEN"], account["ACCESS_TOKEN_SECRET"])
        return tweepy.API(auth)

    def get_user_info(self):
        user_obj = self.tw_api.me()

        result = {}
        result["id"] = user_obj._json["id"]
        result["screen_name"] = user_obj._json["screen_name"]
        return result

    def get_tweets(self):
        return self.tw_api.user_timeline(self.user_info["id"])

    def clean_tweets(self):
        """
        Get 20 most recent tweets from user and delete all.
        """
        tweets = self.tw_api.user_timeline(self.user_info["id"])
        tweet_ids = [status._json["id"] for status in tweets]

        for tw_id in tweet_ids:
            self.tw_api.destroy_status(tw_id)


def test_correct_keyword_no_time_room(l_bot, s_bot, keyword):
    """
    Send a tweet with keyword stream is listening for, but not including 
    a time and room. Should not get @ mention.
    """
    # user sends a tweet containing the correct keyword but not 
    s_tweet = "test 1: {}".format(keyword)
    s_bot.tw_api.update_status(s_tweet)
    time.sleep(5)

    # no action should be taken by l_bot, checking that no retweets sent
    l_tweets = l_bot.get_tweets()
    assert (len(l_tweets) == 0), "tweet where there shouldn't be"

    s_bot.clean_tweets()

def test_correct_keyword_with_room_time(l_bot, s_bot, keyword):
    """
    Send a tweet with room and time that should get @ mention. 
    """
    s_tweet = "test 2: {} @ 6pm room H112".format(keyword)
    s_bot.tw_api.update_status(s_tweet)
    time.sleep(5)

    l_tweets = l_bot.get_tweets()
    assert (len(l_tweets) == 1),"one tweet expected: {} found".format(len(l_tweets))

    mention = "@{}".format(s_bot.user_info["screen_name"])
    assert (mention in l_tweets[0]._json["text"]), "correct user not mentioned"

    s_bot.clean_tweets()
    l_bot.clean_tweets()

def test_adding_bot_to_ignore_list_works_as_expected(l_bot, s_bot, keyword):
    """
    Update ignore list with sending bot's id and then send tweet that should 
    be retweeted, test that listener correctly ignores tweet. 
    """
    # create a new AppConifg model instance with s_bot id in ignore_users
    # app_config should still be set to auto_send: false
    start_conf = model_to_dict(OutgoingConfig.objects.latest("id"))
    test_conf = {
            "auto_send": start_conf["auto_send"],
            "default_send_interval": start_conf["default_send_interval"],
            "ignore_users": [s_bot.user_info["id"]]
            }
    OutgoingConfig.objects.create(**test_conf)

    # send a tweet from s_bot that should get an @ mention
    s_tweet = "test 3: {} @ 6pm room H112".format(keyword)
    s_bot.tw_api.update_status(s_tweet)
    time.sleep(5)

    # check that tweet wasn't sent form listen bot
    l_tweets = l_bot.get_tweets()
    assert (len(l_tweets) == 0), "tweet where there shouldn't be"

    # set OutgoingConfig latest record back to starting state with only id changed
    test_conf["ignore_users"] = []
    OutgoingConfig.objects.create(**test_conf)

    # clean twitter accounts 
    s_bot.clean_tweets()
    l_bot.clean_tweets()

def test_valid_tweet_causes_bot_to_send_retweet_about_event(l_bot, s_bot, keyword):
    """
    This test requires the celery and rabbitmq to be running in the background
    and will send a retweet after the delay time. 
    """
    # turn auto_send on, this will cause a valid tweet to be retweeted
    # a minute after it is recived. 
    test_conf = {
        "auto_send": 1,
        "default_send_interval": 1,
        "ignore_users": []
        }
    OutgoingConfig.objects.create(**test_conf)

    # send a tweet from s_bot that should get an @ mention and retweet 1 min later
    s_tweet = "test 4: {} @ 6pm room H112".format(keyword)
    s_bot.tw_api.update_status(s_tweet)
    print("sleeping to wait for retweet")
    time.sleep(80)

    # check that two tweets have been sent from bot's account
    l_tweets = l_bot.get_tweets()
    assert (len(l_tweets) == 2),"two tweet expected: {} found".format(len(l_tweets))

    s_bot.clean_tweets()
    l_bot.clean_tweets()

def interface(keyword):
    """
    In order for these tests to run correctly they will clear the test
    twitter accounts of all messages at the start and inbetween tests.

    The twitter bot must be running and listening for a unique keyword.
    This keyword should be passed in as a command line arg to this script.

    Celery and Rabbitmq should also be running as normal. 

    The bot maintains the state of ignored users so it must be 
    restarted if running this script more than once. 
    """
    listen_bot = TwitterBot(listener)
    send_bot = TwitterBot(sender)

    # clean both twitter accounts
    listen_bot.clean_tweets()
    send_bot.clean_tweets()

    # setup latest OutgoingConfig object to not auto_send tweets unitl needed
    test_conf = {
        "auto_send": 0,
        "default_send_interval": 1,
        "ignore_users": []
        }
    OutgoingConfig.objects.create(**test_conf)

    #test 1:
    test_correct_keyword_no_time_room(listen_bot, send_bot, keyword)

    #test 2: 
    test_correct_keyword_with_room_time(listen_bot, send_bot, keyword)

    #test 3:
    test_adding_bot_to_ignore_list_works_as_expected(listen_bot, send_bot, keyword)

    #test 4: 
    test_valid_tweet_causes_bot_to_send_retweet_about_event(listen_bot, send_bot, keyword)

def cli_interface():
    """
    wrapper_cli method that interfaces from commandline to function space
    call the script with: 
    python end_to_end.py <keyword: Should be keyword stream is filtering on>
    """
    try:
        keyword = sys.argv[1]

    except:
        print("usage: {} <keyword stream is filering on>".format(sys.argv[0]))
        sys.exit(1)
    interface(keyword)


if __name__ == "__main__":
    cli_interface()