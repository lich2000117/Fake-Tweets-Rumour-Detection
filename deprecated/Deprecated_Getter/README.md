# TweepyAPP
 Using tweepy to scrap twitter's data

## Twitter API:
    Please get the latest twitter API and put them into the config.json to make it work.

## Latest Version:

getTweet.py:
- config.json as configuration file, it specifies the query, max number of tweets and Time_END
- Time_END is a boundary parameter, it automatically captures the oldest tweets that we scratched, next time, the program will only start to scrap BEFORE Time_END date, makes sure we don't repetatively capture the latest tweets over and over again.
- It automatically creates a folder : ./data/Twitter/ 
- It also creates a json file storing all the tweets inside the above folder: tweets.json  


## Deprecated Folder:
Old version of Tweepy API, doesn't work anymore, used to do a research project with Beijing Foreign Language University. Scratch Twitter Tweets , Facebook Posts and do wordCloud analysis etc.