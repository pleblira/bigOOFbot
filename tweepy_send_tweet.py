import os
import tweepy
from get_exclude_reply_user_ids import *
import random


def tweepy_send_tweet(tweet_message,tweet_id, json_response):
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    gif_random_picker = random.randint(1,5)
    
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    exclude_reply_user_ids = get_exclude_reply_user_ids(json_response)
    # api.update_status(tweet_message,in_reply_to_status_id = tweet_id , auto_populate_reply_metadata=True, exclude_reply_user_ids = exclude_reply_user_ids)
    api.update_status_with_media(tweet_message,in_reply_to_status_id = tweet_id , auto_populate_reply_metadata=True, exclude_reply_user_ids = exclude_reply_user_ids, filename = "assets/oof"+str(gif_random_picker)+".gif")