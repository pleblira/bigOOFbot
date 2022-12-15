import requests
import os
import json
from dotenv import load_dotenv, find_dotenv
import webbrowser
from datetime import datetime
from remove_mentions_from_tweet_message import *


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(tweet_id):
    tweet_fields = "tweet.fields=referenced_tweets,attachments,author_id,created_at,entities,id,text&media.fields=preview_image_url,url&expansions=attachments.media_keys,author_id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "ids="+tweet_id
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_tweet_to_reply_to(tweet_id):
    url = create_url(tweet_id)
    json_response_from_reply = connect_to_endpoint(url)
    tweet_id_to_reply_to = "1110302988"
    # print(stackjoinadd_tweet_message)
    # print(json_response_from_reply['data'][0]['referenced_tweets'][0]['id'])
    if 'referenced_tweets' not in json_response_from_reply['data'][0]:
        return None
    for item in json_response_from_reply['data'][0]['referenced_tweets']:
        if item['type'] == "replied_to":
            tweet_id_to_reply_to = item['id']
    
    
    # webbrowser.open('https://twitter.com/halfin/status/'+tweet_id_to_add_to_mempool)
    # return gif_url
    json_response_from_tweet_to_reply_to = connect_to_endpoint(create_url(tweet_id_to_reply_to))
    author_id_tweet_to_reply_to = json_response_from_tweet_to_reply_to['data'][0]['author_id']
    print(f"the json dumps from get tweet to reply to is: \n{json.dumps(json_response_from_tweet_to_reply_to, indent=4, sort_keys=True)}")
    # print(json.dumps(json_response_from_tweet_to_stackjoinadd, indent=4, sort_keys=True))
    # print("\n\n\n")
    # checking if bigOOFbot is the tweet to reply to, or if bigoofbot is mentioned in the reply to tweet
    contains_bigoofbot_on_tweet_to_reply_to_mentions = False
    if author_id_tweet_to_reply_to == "1602113748839317512":
        contains_bigoofbot_on_tweet_to_reply_to_mentions = True
    if "entities" in json_response_from_tweet_to_reply_to['data'][0]:
        if "mentions" in json_response_from_tweet_to_reply_to['data'][0]['entities']:
            for item in json_response_from_tweet_to_reply_to['data'][0]['entities']['mentions']:
                if item['id'] == "1602113748839317512":
                    contains_bigoofbot_on_tweet_to_reply_to_mentions = True
    rebuilding_dict_to_make_it_compatible_with_main = {}
    rebuilding_dict_to_make_it_compatible_with_main['data'] = json_response_from_tweet_to_reply_to['data'][0]
    rebuilding_dict_to_make_it_compatible_with_main['includes'] = json_response_from_tweet_to_reply_to['includes']
    # print(json.dumps(rebuilding_dict_to_make_it_compatible_with_store_stackjoin_function, indent=4, sort_keys=True))
    # print(json.dumps(json_response_from_tweet_to_stackjoinadd, indent=4, sort_keys=True))
    # tweet_datetimeISO = rebuilding_dict_to_make_it_compatible_with_store_stackjoin_function['data']['created_at']
    # tweet_datetimeISO = tweet_datetimeISO[0:tweet_datetimeISO.find(".")]
    return rebuilding_dict_to_make_it_compatible_with_main, tweet_id_to_reply_to, author_id_tweet_to_reply_to, contains_bigoofbot_on_tweet_to_reply_to_mentions

if __name__ == "__main__":
    get_tweet_to_reply_to("1600692890807971840")
    # stackjoin_add("1598477437813260288")

