import os
import json

def returnTweets(folder):
    tweets = []
    # Create path using current directory and folder name
    PATH = os.path.join(os.getcwd(), folder)
    # Iterate through directory for file names
    for file in os.listdir(PATH):
        # Open files using filename and path
        fileDir = os.path.join(PATH, file)
        with open(fileDir, 'r', encoding="utf-8") as f:
            # Save tweet data as json file
            tweet = json.load(f)
            # Only add tweet to list if its not a retweet or reply
            if not tweet['is_retweet'] and not tweet['is_reply']:
                tweets.append(tweet)
    return tweets