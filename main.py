# -*- coding: utf-8 -*-
"""HW2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O8FAG_ktwU2tn7XZ3XEvQu0IYXT04AbJ

Akshit Pal 2017045 


Atieve Wadhwa 2017031


## Library Imports and Global Variables ##
"""

import random
import os
import time
import tweepy
import datetime
import json
import pandas as pd
import csv
import matplotlib as mpl
from geopy.geocoders import Nominatim
import folium

ACCESS_TOKEN = "1214290028701970433-kEuAt1sO18gYwxohZh5l9a2NnJQi8I"
ACCESS_SECRET = "sjWdkpCvzSzWD1JTTNIPDCRgxZQRhHgFs033lAQT5p27c"
CONSUMER_KEY = "8lsE3g44643tDBEj4MSAbQ6rh"
CONSUMER_SECRET = "xTFXRE1ZUloYdtAFrkJqIfe4xUmZ1Q18mEKfOiE2VvEjPGSyAs"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

username = "@HTBrunch"

"""## a) Collecting tweets ##"""

startDate = datetime.datetime(2018, 12, 1, 0, 0, 0)
endDate =   datetime.datetime(2020, 1, 25, 0, 0, 0)

tweets = []
tmpTweets = api.user_timeline(username)
for tweet in tmpTweets:
    if tweet.created_at < endDate and tweet.created_at > startDate:
        tweets.append(tweet)

while (tmpTweets[-1].created_at > startDate):
    tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)

import pickle

tweet_file = open(username + "_tweets_file.bin","wb")
pickle.dump(tweets,tweet_file)
tweet_file.close()

import pickle

tweet_file = open(username + "_tweets_file.bin","rb")
tweets = pickle.load(tweet_file)
tweet_file.close()

"""### Sample Tweets ###

##### Latest Tweet #####
"""

print(tweets[0].created_at)
print(tweets[0].text)

"""##### Random Tweet #####"""

index = random.randint(0,len(tweets))
print(tweets[index].created_at)
print(tweets[index].text)

"""##### Oldest Tweet"""

print(tweets[-1].created_at)
print(tweets[-1].text)

"""## b) Follower Geolocations ##"""

snowden = api.get_user(username)
snowden_id = snowden.id
follower_count = 0

users = []
page_count = 0
for i, user in enumerate(tweepy.Cursor(api.followers, id=snowden_id, count=5000).pages()):
    print("Getting page " + str(i))
    users += user
    follower_count += 1


print("Followers: " + str(follower_count))

users = []

print(follower_count)

import pickle
o_file = open(username+'_followers_file.csv', 'w')
f = csv.writer(o_file, delimiter =',')
f.writerow(["screenname", "name", "location"])

for u in users:
        screenname = u.screen_name.strip()
        name = u.name.strip()
        location = u.location.strip()
        f.writerow([screenname, name, location])

o_file.close()

follower_file = open(username+"_follower_file.bin","wb")
pickle.dump(tweets,follower_file)
tweet_file.close()

"""Plotting top 20 followers due to API limitations"""

pd.options.mode.chained_assignment = None  # default='warn'
df = pd.read_csv(username+'_followers_file.csv', sep = ',')
df = df.dropna(subset=[
  'location'
])
df = df.head(30)
display(df)

from geopy.geocoders import Nominatim
import folium

geolocator = Nominatim(timeout=10, user_agent = 'ubuntu')
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=4, max_retries=2, error_wait_seconds=5.0, swallow_exceptions=True, return_value_on_exception=0)

def get_lat(input_location):
    time.sleep(2)
    location = geolocator.geocode(input_location)
    lat = 0
    if location is not None and location.latitude is not None:
      lat = (location.latitude)

    return lat

def get_lon(input_location):
    time.sleep(2)
    lon = 0
    location = geolocator.geocode(input_location)
    if location is not None and location.longitude is not None:
      lon = (location.longitude)

    return lon

df['latitude'] = df['location'].apply(get_lat)
df['longitude'] = df['location'].apply(get_lon)

print(df.head(5))

df.to_csv(username+"_followers_location.csv")

df = pd.read_csv(username+'_followers_location.csv')
print(df)

mapa = folium.Map()
for index,row in df.iterrows():
    folium.Marker(location=(row['latitude'],row['longitude'])).add_to(mapa)
display(mapa)

"""## c) Top Retweeters ##"""

from collections import Counter
retweeters = []
for tweet in tweets:
  for retweeter in enumerate(tweepy.Cursor(api.retweeters, id=tweet.id).pages()):
    retweeters += retweeter

relist = []
for x in retweeters:
  if isinstance(x,list):
    for z in x:
      relist.append(z)

ledger = Counter(relist)
top_ten = ledger.most_common(10)
top_users  = []
for name,count in top_ten:
  top_users.append(name)
follower_file = open(username+"_follower_file.bin","wb")
pickle.dump(top_users,follower_file)
top_users

follower_file = open(username+"_follower_file.bin","rb")
top_users = pickle.load(follower_file)

udf = pd.DataFrame(top_users,columns=['ID'])

def get_followers(id):
  model = api.get_user(id)
  return model.followers_count

def get_friends(id):
  model = api.get_user(id)
  return model.friends_count

def get_status_count(id):
  model = api.get_user(id)
  return model.statuses_count

def get_verified(id):
  model = api.get_user(id)
  return model.verified

def get_location(id):
  model = api.get_user(id)
  return model.location

def get_created(id):
  model = api.get_user(id)
  return model.created_at

def get_username(id):
  model = api.get_user(id)
  return model.screen_name

udf['Followers'] = udf['ID'].apply(get_followers)
udf['Friends'] = udf['ID'].apply(get_friends)
udf['Statuses'] = udf['ID'].apply(get_status_count)
udf['Verified'] = udf['ID'].apply(get_verified)
udf['Created'] = udf['ID'].apply(get_created)
udf['Location'] = udf['ID'].apply(get_location)
udf['Latitude'] = udf['Location'].apply(get_lat)
udf['Longitude'] = udf['Location'].apply(get_lon)

udf['Handle'] = udf['ID'].apply(get_username)
udf.to_csv(username+'_top_fans.csv')
udf

udf = pd.read_csv(username+'_top_fans.csv')
udf

"""#### Locations ####"""

mapa = folium.Map()
for index,row in udf.iterrows():
    folium.Marker(location=(row['Latitude'],row['Longitude'])).add_to(mapa)
display(mapa)

"""#### Friends vs Followers ####"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

handles = udf['Handle'].tolist()
friends = udf['Friends'].tolist()
followers = udf['Followers'].tolist()

import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Bar(name='Friends', x=handles, y=friends),
    go.Bar(name='Followers', x=handles, y=followers)
])
# Change the bar mode
fig.update_layout(barmode='stack')
fig.show()

"""#### Account Age ####"""

import plotly.express as px
from datetime import datetime
dates = udf['Created'].tolist()
now = datetime.now()
age = []
for dt in dates:
  age.append((now-datetime.strptime(dt,'%y-%m-%d %H:%M:%S')).days/365)
fig = px.scatter(x=handles, y=age)
fig.update_layout(
    title="Age distribution of top retweeters",
    xaxis_title="User handle",
    yaxis_title="Account Age in Years",
)
fig.update_traces(mode='markers+lines', marker_line_width=2, marker_size=10)
fig.show()

"""## d) Tweet Frequency ##"""

import pickle

tweet_file = open(username + "_tweets_file.bin",'rb')
tweets = pickle.load(tweet_file)
#print(tweets[0])

from collections import Counter
weekly = []
monthly = []
hourly = []
for tweet in tweets:
  time = tweet.created_at
  weekly.append(time.weekday())
  monthly.append(time.month)
  hourly.append(time.hour)

week_freq = (Counter(weekly))
month_freq = (Counter(monthly))
hour_freq = (Counter(hourly))

plt.figure(figsize=(10,8))
plt.bar(hour_freq.keys(),hour_freq.values())
plt.title("Hourly tweeting frequency")
plt.ylabel("Number of Tweets")
plt.xticks([0,6,12,18],['12AM', '6AM', '12PM', '6PM'])
plt.show()

plt.figure(figsize=(10,8))
plt.bar(week_freq.keys(),week_freq.values())
plt.title("Day wise tweeting frequency")
plt.xticks(np.arange(7),['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.ylabel("Number of Tweets")
plt.show()

plt.figure(figsize=(10,8))
plt.bar(month_freq.keys(),month_freq.values(),)
plt.title("Monthly tweeting frequency")
plt.ylabel("Number of Tweets")
plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()

"""## e) Engagement Score"""

import pickle
from datetime import datetime
from dateutil.parser import parse

tweet_file = open(username + "_tweets_file.bin",'rb')
tweets = pickle.load(tweet_file)
#print(tweets[0].created_at.utcnow().date())
p = 0
tweetdf = pd.DataFrame(columns=['id','created_at','retweet_count','favorite_count','reply_count','text','photo','video'])

for tweet in tweets:
    d = tweet.created_at.date()
    d = d.strftime('%Y-%m-%d')
    #date = parse(d)
    #print(date)
    r = -1
    if hasattr(tweet,'reply_count'):
        r = tweet.reply_count
    else:
        r = 0
    text = 0
    photo = 0
    video = 0
    if not hasattr(tweet,'extended_entities'):
        text =1
    else:
        l = tweet.extended_entities['media'][0]
        if(l['type']=='video'):
          video = video+1
        if(l['type']=='photo'):
          photo = photo +1
    tweetdf = tweetdf.append({'id':tweet.id,'created_at':d,'retweet_count':tweet.retweet_count,'favorite_count':tweet.favorite_count,'reply_count':r,'text':text,'photo':photo,'video':video},ignore_index=True)

tweets_per_day = tweetdf['created_at'].value_counts()
datedf = tweets_per_day.reset_index()
datedf.columns = ['date','count']
#print(datedf)
print(tweetdf.head())

# E_Score = (2*Retweets+Replies+Likes)*2*(No. of posts that day)/Total no. of posts

x = [b for b in range(0,len(tweetdf))]
e_score = []
for i in range(len(tweetdf)):
    date = tweetdf.iloc[i]['created_at']
    p = (datedf[datedf['date']==date]['count'])
    posts = (p.iloc[0])
    score = (2*tweetdf.iloc[i]['retweet_count']+tweetdf.iloc[i]['reply_count']+tweetdf.iloc[i]['favorite_count'])*2*posts/len(tweetdf)
    e_score.append(score)
mpl.pyplot.scatter(x,e_score)
mpl.pyplot.show()
tweetdf['Engagement Score'] = e_score
#print(tweetdf['Engagement Score'])

text_df = tweetdf[tweetdf['text']==1].reset_index(drop=True)
text_df = text_df.sort_values(by='Engagement Score', ascending=False)
text_df = text_df.iloc[:20,:]
#print(text_df['favorite_count'].max())

photo_df = tweetdf[tweetdf['photo']==1].reset_index(drop=True)
photo_df = photo_df.sort_values(by='Engagement Score', ascending=False)
photo_df = photo_df.iloc[:20,:]
#print(photo_df)

video_df = tweetdf[tweetdf['video']==1].reset_index(drop=True)
video_df = video_df.sort_values(by='Engagement Score', ascending=False)
#video_df = photo_df.iloc[:20,:]
#print(video_df)

import matplotlib.pyplot as plt
retweet_sum = [text_df['retweet_count'].sum()/20,photo_df['retweet_count'].sum()/20,video_df['retweet_count'].sum()/3]
like_sum = [text_df['favorite_count'].sum()/20,photo_df['favorite_count'].sum()/20,video_df['favorite_count'].sum()/3]
#print(retweet_sum)
e_sum = [text_df['Engagement Score'].sum()/20,photo_df['Engagement Score'].sum()/20,video_df['Engagement Score'].sum()/3]
plt.figure(figsize=(9, 5))
plt.subplot(131)
plt.bar([1,2,3],retweet_sum)
plt.ylabel("Avg. Number of retweets per post")
plt.xticks([1,2,3],['Text','Photo','Video'])
plt.subplot(132)
plt.bar([1,2,3],like_sum)
plt.ylabel("Avg. Number of likes per post")
plt.xticks([1,2,3],['Text','Photo','Video'])
plt.subplot(133)
plt.bar([1,2,3],e_sum)
plt.ylabel("Avg. Engagement Score per post")
plt.xticks([1,2,3],['Text','Photo','Video'])
plt.show()

"""## f) Major topics ##

Word Cloud
"""

import pickle
import json, random
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import scipy

tweet_file = open(username + "_tweets_file.bin",'rb')
tweets = pickle.load(tweet_file)

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

words = ' '
for tweet in tweets:
  words += tweet.text

stopwords = {'https',"co","RT"}

wordcloud = WordCloud(
    stopwords=STOPWORDS.union(stopwords),
    background_color='black',
    max_words=500,
    width=7000,
    height=7000
).generate(words)

plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3))
plt.axis('off')
plt.savefig('./tweetcloud2.png', dpi=300)
plt.show()

"""Top Hashtags"""

hashtags_dict = {}
for tweet in tweets:
        hashtags = tweet.entities.get('hashtags')
        for hashtag in hashtags:
            if hashtag['text'] in hashtags_dict.keys():
                hashtags_dict[hashtag['text']] += 1
            else:
                hashtags_dict[hashtag['text']] = 1

answers = sorted(hashtags_dict, key=hashtags_dict.get, reverse=True)
for i in range(0,10):
  print( str(i+1) + ") #" + answers[i] + ": "+str(hashtags_dict[answers[i]]))

"""Tweet Length Comparison"""

import matplotlib.pyplot as plt

lengths = []
for tweet in tweets:
  lengths.append(len(tweet.text))

x = [b for b in range(0,len(tweets))]

plt.scatter(x,lengths)
plt.title("Lengths of Tweets")
plt.xlabel("Tweet Number")
plt.ylabel("Length")
plt.rcParams["figure.figsize"] = (5,5)
plt.show()