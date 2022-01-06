#!/bin/python3

"""
This script leveraged the tweepy library to collect tweets
every 3 minutes during the presidential debate on 9/29/2020.
Tweets are stored in a DataFrame object and saved locally to a CSV

Ian Richard Ferguson
"""

# ---- Imports
import tweepy, time
import pandas as pd
from datetime import datetime
from twilio.rest import Client


# ---- Setup API connection
login = {"consumerKey":"XXXX",                                                  
        "consumerSecret":"XXXX",
        "accessKey":"XXXX",
        "accessSecret":"XXXX"}

# Connect to Twitter API
auth = tweepy.OAuthHandler(consumer_key = login["consumerKey"],
                           consumer_secret = login["consumerSecret"])

auth.set_access_token(key = login["accessKey"],
                      secret = login["accessSecret"])

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

# Test connection
try:
    api.verify_credentials()
    print("Blue Check")

except:
    print("Nah fam")


# ---- Helpers
def scraper(target, count, NOW):
    """
    target => Biden or Trump, keyword search
    count => # of tweets that will be scraped
    NOW => Time that collection started for this iteration

    This function scrapes recent tweets for a target subject and stores them
    in a Pandas DataFrame object. Returns a DataFrame
    """

    # Empty lists that we'll use as temporary containers
    today, created, name, location, text, likes, rts = [], [], [], [], [], [], []

    # Filter out Retweets and hyperlinks
    queryTarget = target + " -filter:retweets -filter:links"

    for tweet in tweepy.Cursor(api.search, q =queryTarget, lang ='en',
                               tweet_mode='extended', result_type='recent').items(count):

        # Push to lists
        today.append(datetime.now().strftime("%m-%d-%Y"))
        created.append(tweet.created_at)
        name.append(tweet.user.name)
        location.append(tweet.user.location)
        text.append(tweet.full_text)
        likes.append(tweet.favorite_count)
        rts.append(tweet.retweet_count)

    # Assign lists to columns in Pandas dataframe
    tweetData = pd.DataFrame({'Today':today,'Created': created,
                              'User Name': name, 'Location': location,
                              'Tweet': text, 'Likes': likes, 'Retweets': rts})

    tweetData["TARGET"] = target
    tweetData["TIME"] = NOW
    
    return tweetData


def allDone():
    """
    This function sends a text to my phone when the script finishes.

    Why? Why not!
    """

    client = Client("XXXX", "XXXX")
    MY_NUMBER = "XXXXX"

    msg = "Hey big guy,\n\nYour app is all finished running. Congrats on a job well done! (Probably)"

    client.messages.create(to="XXXXX",
                           from_=MY_NUMBER,
                           body=msg)


# ---- Exececute
candidates = ["Biden", "Trump"]

end = datetime(2020, 9, 29, 21, 0, 0, 0)

# Empty DataFrame to append into
output = pd.DataFrame()

# Tracking variable to use to break the loop
k=0

while k <= 65:
    
    """
    We'll complete 66 iterations of Tweet collections throughout debate night
    """

    print("Starting iteration {}....".format(str(k+1)))
    now=datetime.now()
    
    for candidate in candidates:
        output=output.append(scraper(candidate, 50, NOW=now), ignore_index=True)
    
    print("Completed iteration {}....".format(str(k+1)))
    
    print("Sleeping for 3m....")
    time.sleep(180)
    
    k += 1

output.to_csv("DEBATE-output.csv", index=False)
print("All done!")
allDone()
