import tweepy
import datetime
import csv
import re
import json
import time
import os.path
import pytz
from datetime import timedelta


consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def collect_tweets_data(screen_name):

    tz = pytz.timezone('US/Central')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    tweets_list = []
    final_tweet_list = []

    tweet_in = api.user_timeline(screen_name=screen_name,tweet_mode="extended", include_rts = True, count=50)

    tweets_list.extend(tweet_in)

    oldest = tweets_list[-1].id - 1
    tweetid = 0
    for tweet in tweet_in:
        tweetid = tweetid + 1
        tweet_id = "tweet"+str(tweetid)
        tweet_container = []

        try:
            likes = tweet.favorite_count
        except:
            likes = "0"

        try:
            hashtag = len(tweet.entities[u'hashtags'][0])

        except:
            hashtag = "0"

        # RETWEET COUNT
        try:
            retweets = tweet.retweet_count
        except:
            retweets = "0"
    
        tweet_container.append(tweet.author.name.encode("utf-8"))
        tweet_container.append(tweet.author.statuses_count)
        tweet_container.append(tweet.author.friends_count)  
        tweet_container.append(tweet.author.followers_count)  
        tweet_container.append(tweet.author.favourites_count) 
                                                        
        tweet_container.append(tweet.author.listed_count)
        tweet_container.append(tweet_id)
        
        urlfortweet = "https://twitter.com/"+screen_name+"/status/"+str(tweet.id)
        urlfortweet = str(urlfortweet)
        urlfortweet = urlfortweet.encode("utf-8")
        tweet_container.append(urlfortweet)
        
        tweet_container.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        t_created_at = tweet.created_at - timedelta(hours=8)
        tweet_container.append(t_created_at)
        
        media_files = []
        
        if hasattr(tweet, 'retweeted_status'):
            media = tweet.retweeted_status.entities.get('media', [])
            if(len(media)>0):
                media_files.append(media[0]['media_url'])
            tweet_container.append(1)
            retweet = tweet.retweeted_status.author.name   
            tweet_container.append(retweet.encode("utf-8"))
        else:
            media = tweet.entities.get('media', [])            
            if(len(media) > 0):
                media_files.append(media[0]['media_url'])
            tweet_container.append(0)
            tweet_container.append(None)
            
            
        tweet_container.append(likes)
        tweet_container.append(retweets)
                                                            

        tweet_container.append(tweet.full_text.encode("utf-8")) 
        videos = []
        pictures =[]
        # -- Picture count ---
        for i in range(len(media_files)):
            if "video" in media_files[i]:
                videos.append(media_files[i])
            else:
                pictures.append(media_files[i])

        tweet_container.append(len(pictures)) 
        tweet_container.append(len(videos)) 

        tweet_container.append(hashtag)

        #links
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.full_text)
        links = []
        for url in urls:
            links.append(url)
        tweet_container.append(len(links))

         #hastag1 2 3 4 5
        hashtagvalue = tweet.entities.get('hashtags')
        hashtags = []
        if len(hashtagvalue)>0:
            for i in range(len(hashtagvalue)):
                if any('text' in d for d in hashtagvalue):
                    hashtags.append(hashtagvalue[i]['text'])
                else:
                    hashtags = []
        else:
            hashtags = []

        if len(hashtags)>0:
            if len(hashtags)==5:
                for i in range(0,5):
                    tweet_container.append(hashtags[i].encode("utf-8"))
            elif len(hashtags)< 5:
                count = 5 - len(hashtags)
                for j in range(len(hashtags)):
                    tweet_container.append(hashtags[j].encode("utf-8"))
                for j in range(0,count):
                    tweet_container.append(" ")
        else:
            for i in range(0,5):
                if i>4:
                    break
                else:
                    tweet_container.append(" ")
        if len(links)>0:
            if len(links)==3:
                for i in range(0,3):
                    tweet_container.append(links[i].encode("utf-8"))
            elif len(links)< 3:
                count = 3 - len(links)
                for j in range(len(links)):
                    tweet_container.append(links[j].encode("utf-8"))
                for j in range(0,count):
                    tweet_container.append(" ")
        else:
            for i in range(0,3):
                if i>2:
                    break
                else:
                    tweet_container.append(" ")        
        
        final_tweet_list.append(tweet_container)

    with open('tweeterScrapper.csv', 'a', newline ='') as f:
        writer = csv.writer(f)    
        writer.writerows(final_tweet_list)

    pass



if __name__ == '__main__':
    page_id = ["jairbolsonaro"]
    flag = 0
    now = datetime.datetime.now()
    print("Data collected for time: ",now)
    if os.path.isfile('tweeterScrapper.csv'):
        with open('tweeterScrapper.csv', 'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([" "," "])
            writer.writerow(["","","",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        for i in page_id:
            collect_tweets_data(i)
            time.sleep(1)
        flag = 1
        time.sleep(0)
    else:
        with open('tweeterScrapper.csv', 'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Account", "#Tweets", "#Following", "#Followers", "#Likes", "#lists", "tweetid","url", "Data Collected","created_time", "Retweeted", "RetweetFrom","#likes","#retweets","texts","picture", "video","#Hashtag","links", "hashtag1", "hashtag2", "hashtag3", "hashtag4","hashtag5","link1", "link2","link3"])
        for i in page_id:
            collect_tweets_data(i)
            time.sleep(1)
        flag = 1
        time.sleep(0)

