# A Python Script making use of Twitter's API to do scraping on tweets, Analyse Word Frequency
# Written by Chenghao Li 
# 07/02/2021

from util_functions import *

import tweepy
from tweepy import OAuthHandler
import json
import os

cur_dir = os.getcwd()
config_filePATH = os.path.join(cur_dir,"config.json")
parent_dir = os.path.join(cur_dir,"data")
sav_dir = os.path.join(parent_dir,"Twitter")
#-------------------------------------------------------OUT PUT FILE config---------------------------------------------------------#
OUT_JSON_NAME = os.path.join(sav_dir,"twitter.json")
# make directory if not exist
os.makedirs(os.path.dirname(OUT_JSON_NAME), exist_ok=True)
#----------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------------Search Option config---------------------------------------------------------#

# Load Data
#Load exclude list when calculating frequency
with open(config_filePATH) as f:
    config_file = json.load(f)
    CONSUMER_KEY = config_file["CONSUMER_KEY"]
    CONSUMER_SECRET = config_file["CONSUMER_SECRET"]
    ACCESS_TOKEN = config_file["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = config_file["ACCESS_TOKEN_SECRET"]
    QUERY = config_file["Query"]
    MAX_COUNT = int(config_file["MaxTweet"])
    TIME_END = config_file["Time_END"]
    if not TIME_END:
        TIME_END = str(get_current_time())[0:10]
#----------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------Twitter API Setup-------------------------------------------------------------#
# Twitter Token
consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET
# create OAuthHandler object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)
#----------------------------------------------------------------------------------------------------------------#


def Extend_Json(new_dict, File_PATH):
    """Extend a huge json file without loading it to the memory"""
    # if file exists:
    if os.path.exists(File_PATH):
        if new_dict: # if dict has value
            # Source: https://stackoverflow.com/questions/18087397/append-list-of-python-dictionaries-to-a-file-without-loading-it/31224105#31224105?newreg=6b7713ed96df42959bb9443daf7bb8ec
            # two methods
            # with open (File_PATH, mode="r+") as file:
            #     file.seek(0,2)  # 0 byte (0) from the end of file (2)
            #     position = file.tell() -1
            #     file.seek(position)
            #     file.write( ",{}]".format(json.dumps(new_dict)) )
            with open (File_PATH, mode="r+") as file:
                file.seek(os.stat(File_PATH).st_size -1)
                file.write( ",{}]".format(json.dumps(new_dict, indent=2)) )
    else:
        # else, create a new json file
        with open (File_PATH, mode="w") as file:
            json.dump(new_dict, file, indent=2)

def Update_Config(new_config_dict, config_filePATH):
    """Update Configuration file, mainly because we only keep tweets published before the last tweets we scratched."""
    with open (config_filePATH, mode="w") as f:
        json.dump(new_config_dict, f, indent=2)
    
#-------------------------------------------------Function List---------------------------------------------------------------#

#Function that search tweets and save it in dictionary, and set, output to doc file.
def Get_Tweet(api, data_list_of_dict, data_set):
    for tweet in tweepy.Cursor(api.search_tweets, q=QUERY, until=TIME_END, include_entities=True, tweet_mode="extended").items(MAX_COUNT):
        id = tweet.id
        # try different types of method to handle different types of return
        txt = tweet.full_text  # extract full txt when tweet_mode is set to extended
        ## Example: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets#example-response
        time = tweet.created_at
        tweet.entities["hashtags"]
        txt = Remove_URL(txt)
        data_list_of_dict.append({"id": str(id), "created_at": str(time), "user": tweet.user.name, "text": txt})
        data_set.add(txt)
        config_file["Time_END"] = str(time)[0:10]  # update config file to include the oldest tweets we currently reached, to avoid duplicates in the future







#----------------------------------------------------------------------------------------------------------------#





#--------------------------------------------------Main Function--------------------------------------------------------------#

def main():
    data_list_of_dict = []  # A list of dict containing username, create time, full_text
    data_set = set()   # A Set containing all tweet.full_text
    ## Get Tweet and put original tweets into jsonfile.
    Get_Tweet(api, data_list_of_dict, data_set)
    Extend_Json(data_list_of_dict, OUT_JSON_NAME)
    ## Update configuration file to include the oldest tweets time
    Update_Config(config_file, config_filePATH)

#--------------------------------------------------Run--------------------------------------------------------------#
if __name__ == "__main__":
    main()

#----------------------------------------------------------------------------------------------------------------#