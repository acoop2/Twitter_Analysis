#!/usr/local/bin/python3
#This is a python script used to collect tweets using the twitter api "tweepy". With tweepy we can
#ask twitter for the attributes of tweets such as "date", "retweets", "verified", "username", "location", "description"
#the tweet id's were gathered from zonodo a data colletcion site that collect tweet id's or particular subjects


#from loginInfo import *
from datetime import datetime
import time
import tweepy
import sys
import csv
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
import json



#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# Authenticate to Twitter

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

dt=datetime.today()
fileName='tweets_data.csv'
csvFile = open(fileName, 'a', newline='')

#Use csv writer to post results, as well as insert the column names
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["Id","Created_At","Content","Username","Screen_Name","User_Location","User_Description","User_Follower_Count","User_Friend_Count","User_Favorites_Count","Verified"])

#authenticating credentials
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    quit()


#Reading in tweet id's from json file
tweet_dic = []
with open('filename.txt')as r:
    files = r.readlines()
    for i in files:
        c=0
        print("loading" + str(i))
        with open(str(i).strip('\n')) as f:
            lines= f.readlines()
            for i in lines:
                #collect no more than 100,000 tweets
                if (c <= 100000):
                    i = json.loads(i)
                    tweet_dic.append(i['tweet_id'])
                    c+=1
                else:
                    pass

#The twitter api call allows you to query 100 tweets at a time. So we keep an index of 100 to be able to make the api call
a= 0
b=100
count = 0
l = len(tweet_dic)
while(count<=l):
    print("Retrieving Tweets .....")
    try:
        tweet_lis = api.lookup_statuses(tweet_dic[a:b])
    # Write a row to the CSV file. I use encode UTF-8

        try:
            for tweet in tweet_lis:
                try:
                    #write the individual tweet and its attributes to  a row in a csv file
                    csvWriter.writerow([tweet.id, tweet.created_at, tweet.text.encode("utf-8"), tweet.user.name, tweet.user.screen_name, tweet.user.location, tweet.user.description, tweet.user.followers_count,tweet.user.friends_count,tweet.user.favourites_count,tweet.user.verified]) #"tweet.entities"])
                    count+=1
                except:
                    pass
            a+=100
            b+=100
            print(str(count) + " out of "+  str(l) + " donwloaded")



        except Exception as E:
            print(E)
            a+=100
            b+=100
            pass
    #error handler to account for invalid id's or twitter accounts
    except Exception as E:
        print("100 tweets lost")
        print(E)
        a+=100
        b+= 100
        pass
csvFile.close()
