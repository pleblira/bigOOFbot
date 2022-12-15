import tweepy
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json
from datetime import datetime, timedelta
from bearer_oauth import *
from get_rules import *
from delete_all_rules import *
from set_rules import *
from create_throttle_list import *
from clean_up_and_save_recent_interactions import *
from get_exclude_reply_user_ids import *
from tweepy_send_tweet import *
from get_tweet_message import *
from store_stackjoin import *
from get_tweet_to_reply_to import *
import time
from remove_mentions_from_tweet_message import *
import random

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")

throttle_time = 60

def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=author_id,attachments.media_keys&media.fields=url", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code == 429:
        print("ran into error 429 so waiting for 30 seconds for connection to be reset")
        time.sleep(30)
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    if response.status_code != 200 and response.status_code != 429:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(f"\n\n\n\n\n--- --- --- INCOMING TWEET --- --- ---\n")
            print(f"the json dumps for json_response {json.dumps(json_response,indent=4)}\n\n")
            
            oof_phrase_list = ["oof, BIG OOF", "ooooooooof", "ooooof", "BIG OOF", "OOOooOOoOooF", "oof...", "big, big oof"]
            oof = random.choice(oof_phrase_list)

            tweet_id = json_response["data"]["id"]

            data_from_tweet_to_reply_to = get_tweet_to_reply_to(tweet_id)
            if data_from_tweet_to_reply_to != None:
                author_id_tweet_to_reply_to = data_from_tweet_to_reply_to[2]
                # replying to person that quoted the bot and not directly to the mentioned tweet as it didn't make much sense to have a call to a bot just hanging in the tweet without the bot responding
                # tweet_id_to_reply_to = data_from_tweet_to_reply_to[1]
                tweet_id_to_reply_to = tweet_id
                tweet_message = data_from_tweet_to_reply_to[0]["data"]["text"]
                tweet_message = remove_mentions_from_tweet_message(tweet_message)
                tweet_message = tweet_message.upper()
            # this is in case the bot is called on a new tweet that isn't a reply originally
            else:
                author_id_tweet_to_reply_to = json_response["data"]["author_id"]
                tweet_id_to_reply_to = tweet_id
                tweet_message = json_response["data"]["text"]
                tweet_message = remove_mentions_from_tweet_message(tweet_message)
            # checking if it's a reply to a bigOOFbot tweet
            if author_id_tweet_to_reply_to == "1602113748839317512":
                tweet_id_to_reply_to = tweet_id
                tweet_message = json_response["data"]["text"]
                tweet_message = remove_mentions_from_tweet_message(tweet_message)
            # stripping http code that's added to tweet message when there's an image
            if "https://t.co/" in tweet_message[tweet_message.rfind(" "):].lower():
                print("found http on tweet message")
                tweet_message = tweet_message[:tweet_message.rfind(" ")]
            # removing last period of mentioned tweet
            if tweet_message[len(tweet_message)-1:len(tweet_message)] == ".":
                tweet_message = tweet_message[:len(tweet_message)-1]            
            tweet_message = "\""+tweet_message.upper()+"\""+"?!\n\n"+oof

            bigoofbot_mentioned_in_tweet_message = False
            if "@bigoofbot" in tweet_message.lower():
                bigoofbot_mentioned_in_tweet_message == True

            # print(f"json dumps for get_stream: {json.dumps(json_response, indent=4, sort_keys=True)}")
            # processing tweet message
            # tweet_message = json_response["data"]["text"]
            # if tweet_message.strip()[0:len(tweet_message)-9] == (tweet_message.strip()[0:tweet_message.lower().find("fewbot21")-8]):
            #     tweet_message = "Few"
            # else:
            # tweet_message = tweet_message[tweet_message.lower().find("fewbot21")+10:]
            # replace_dictionary = {"?":"",",":"",":":"","!":"","you":"I",".":""}
            # for element_to_replace in replace_dictionary:
                # tweet_message = tweet_message.replace(element_to_replace,replace_dictionary[element_to_replace])
            # tweet_message = tweet_message.strip() + "?\n\nFew"
            # Making all replies "Few" or something else
            # tweet_message = "oof"
            # tweet_message = "Acknowledged by Stackchain bot ✅ (proof of concept)"
            # tweet_message = get_tweet_message(json_response, tweet_message)
            print(tweet_message)

            throttle_list = create_throttle_list(throttle_time)

            tweet_y = False
            tweet_n = False

            while not tweet_y and not tweet_n:
                # additional check for hashtag on text of the tweet (the API has been serving replies to the actual hashtag tweet, which does not apply)
                # if "#stackchain" not in json_response['data']['text'].lower() and "#stackchaintip" not in json_response['data']['text'].lower() and "#stackjoin" not in json_response['data']['text'].lower() and "#pbstack" not in json_response['data']['text'].lower() and "#stackjoinadd" not in json_response['data']['text'].lower():
                #     print("switching tweet_n to True since text doesn't contain hashtags")
                #     tweet_n = True
                if data_from_tweet_to_reply_to[3] == True and bigoofbot_mentioned_in_tweet_message == False:
                    print("the tweet is a reply to a tweet that previously mentioned the bot, so setting tweet_n to True")
                    tweet_n = True
                for throttle_item in throttle_list:
                    print(f"\nthis is an item from throttle_list: {throttle_item}")
                    if json_response['data']['author_id'] in throttle_item:
                    # if item['id'] in throttle_item:
                        print(f"the item id is {json_response['data']['author_id']}")
                        # print(f"the throttle list is {throttle_list}")
                        print("item found in throttle list, don't tweet")
                        tweet_n = True
                    else:
                        print(f"the item id is {json_response['data']['author_id']}")
                        print("not found in throttle list")
                if not tweet_n:
                    tweet_y = True
                print(f"tweet_y: {tweet_y}, tweet_n: {tweet_n}")
                print("\n")
            if tweet_y == True:
                tweepy_send_tweet(tweet_message,tweet_id_to_reply_to, json_response)
                clean_up_and_save_recent_interactions(json_response, throttle_time)
            else:
                print("tweet won't go out and cleaning up recent interactions was skipped")


def main():
    rules = get_rules(bearer_oauth)
    delete_all_rules(rules, bearer_oauth)
    set = set_rules(bearer_oauth)
    get_stream(set)

if __name__ == "__main__":
    main()
    # clean_up_and_save_recent_interactions(json_response)