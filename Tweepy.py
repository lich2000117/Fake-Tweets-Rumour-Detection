import tweepy
import numpy as np
import time
import json
import os

DATA_PATH = "./id_data/train.data.txt"   # train
DEV_DATA_PATH = "./id_data/dev.data.txt"  # dev

AUTHOR_JSON_PATH = "./full_data/author_ids.json"

SOURCE_STORY_ONLY = False
if SOURCE_STORY_ONLY:
    JSON_PATH = "./full_data/full_source_only.json"   # SOURCE_STORY_ONLY=True
else:
    JSON_PATH = "./full_data/full_dev_train.json"

## Twitter API V1.1
consumer_key = "PCyRF0jWO12cgQ88uQDkDoBes"  # API_Key and secret
consumer_secret = "whVymp4fEIeKQEy1hrDghwRxKyW515QeUzFKq5fMvryoe1mOxT"
access_token = "1357932194019217410-RmO2xXuajMNs98s6qw5DYHLAFzMcLZ"
access_token_secret = "ptzYrYJF10qnGf8vU9wPdiuRNOAM3BXFxjMhOcxBZZcKz"

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)
# If the authentication was successful, this should print the
# screen name / username of the account
print(api.verify_credentials().screen_name)

def Extend_Json(new_list_dict, File_PATH):
    """Extend a huge json file without loading it to the memory, input: new_dict is a list of json dictionary objects"""
    # if file exists:
    if os.path.exists(File_PATH):
        if os.stat(File_PATH).st_size == 0:
            print("asasdasdasd")
            # if file contains nothing, delete the file
            os.remove(File_PATH)
            # create another new json file
            with open (File_PATH, mode="w") as file:
                json.dump(new_list_dict, file, indent=2)
        else:
            if new_list_dict: # if dict has value
                with open (File_PATH, mode="r") as file:
                    data = json.load(file)
                # Source: https://stackoverflow.com/questions/18087397/append-list-of-python-dictionaries-to-a-file-without-loading-it/31224105#31224105?newreg=6b7713ed96df42959bb9443daf7bb8ec
                # two methods
                # with open (File_PATH, mode="r+") as file:
                #     file.seek(0,2)  # 0 byte (0) from the end of file (2)
                #     position = file.tell() -1
                #     file.seek(position)
                #     file.write( ",{}]".format(json.dumps(new_dict)[1:-1]) )
                with open (File_PATH, mode="r+") as file:
                    file.seek(os.stat(File_PATH).st_size -1)
                    file.write( ",{}]".format(json.dumps(new_list_dict, indent=2)[1:-1]) )
    else:
        # else, create a new json file
        with open (File_PATH, mode="w") as file:
            json.dump(new_list_dict, file, indent=2)



train_id_list = []
with open(DATA_PATH, "r") as f:
    for line in f:
        line = line.strip() # remove next line
        if SOURCE_STORY_ONLY:
            line = line.split(',')[0] # split into list\
        else:
            line = line.split(',')
        train_id_list.append(line)
if not SOURCE_STORY_ONLY:
    train_id_list = [item for sublist in train_id_list for item in sublist] # Flat into a single list
train_id_list = list(set(train_id_list))
len(train_id_list)

dev_list = []
with open("./id_data/dev.data.txt", "r") as f:
    for line in f:
        line = line.strip() # remove next line
        if SOURCE_STORY_ONLY:
            line = line.split(',')[0] # split into list\
        else:
            line = line.split(',')
        dev_list.append(line)
if not SOURCE_STORY_ONLY:
    dev_list = [item for sublist in dev_list for item in sublist] # Flat into a single list
dev_list = list(set(dev_list))
len(dev_list)

total_id_list = set(train_id_list + dev_list)
len(total_id_list)

def get_twitter_v2(api, list_ids, JSON_PATH):
    """Automatically get a list of tweeters, the function auto divide ids into chunks of size 800 to avoid excessive use of API,
        auto create a Json file in the designated path."""
    ## Auto divide into sub-tasks
    list_ids = list(set(list_ids))
    output_list = []   # output list of dictionary of tweets
    count = 0
    for tweet_id in list_ids:
        ## Main loop to get twitter by chunks
        
        
        # This endpoint/method returns a variety of information about the Tweet(s)
        # specified by the requested ID or list of IDs
        # By default, only the ID and text fields of each Tweet will be returned
        # Additional fields are retrieved using the tweet_fields parameter, selected by hands to make sure we capture useful informations
        try:
            response = api.get_status(id=tweet_id)
        except tweepy.errors.TooManyRequests:
            # if hit rate limit, sleep 15 minutes
            print("Count: ", count)
            print("Hit Rate Limit, Sleep 15 minutes")
            time.sleep(900)
            response = api.get_status(id=tweet_id)
        except:
            # If can't find that ID tweet, or other reasons skip
            count += 1
            continue

        output_list.append(response._json)
        # Save to json file
        
        # Sleep 15 minutes to avoid API restrictions after processing 900 tweets
        #if loop_count == 8: 
            #time.sleep(15*60)
            #loop_count = 0
        if count>999 and count % 1000 == 0:
            Extend_Json(output_list, JSON_PATH)
            print("Saved to File! Current index of list: ", count)
            output_list = [] # reset output list to free memory
        count += 1
    Extend_Json(output_list, JSON_PATH)
    print("Total Tweeter :", count)
        

# Run getter.
get_twitter_v2(api, total_id_list, JSON_PATH)

with open(JSON_PATH, "r") as f:
    data = json.load(f)
    print("Number of twitter stored: ", len(data))