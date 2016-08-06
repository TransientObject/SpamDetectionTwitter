from __future__ import division
import tweepy
import json
import simplejson
from array import *
from twitter import *
import jsonpickle
import inspect
from twython import Twython
import os
from tweepy.parsers import RawJsonParser
import pdb
import re
from dateutil import parser
import csv
import sys
import logging
import shutil
import numpy
import time

def get_auth(index=0):
    #auth values and tokens comes here

    consumer_key=consumer_key_array[index]
    consumer_secret=consumer_secret_array[index]
    access_token=access_token_array[index]
    access_token_secret=access_token_secret_array[index]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

class StreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print "Ran on_status"

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_data(self, data):
        print data
        return True
    
user_ids = []

def print_rate_limits():
    #cleanup code
    limit = api.rate_limit_status()
    print limit['resources']['followers']
    print limit['resources']['friends']
    print limit['resources']["statuses"]["/statuses/mentions_timeline"]

def write_to_file(users_info, path):
    element_file = open(path, 'and')
    for user_info in users_info:
        element_file.write(json.dumps(user_info, sort_keys=True) + "\n")
    element_file.close()


def get_99_users(element_ids, peer_list):
    users_info = json.loads(api_raw.lookup_users(user_ids=element_ids))
    for user_info in users_info:
        peer_list.append(user_info)
    return peer_list

def write_peer_info(iterator, path):
    element_ids = []
    peer_list = []
    for element in iterator:
        dict_var = element.__getstate__()
        dict_var.pop("status", None)
        dict_var.pop("created_at", None)
        dict_var.pop("author", None)
        dict_var.pop("user", None)
        peer_list.append(json.dumps(dict_var))
    print len(peer_list)
    write_to_file(peer_list, path)
    return peer_list

def insert_into_csv(list, size=None):
    global csv_row
    if (len(list) == 0):
        csv_row.extend((0,0,0,0))
        return    
    if size is None:
        size = len(list)
    list = sorted(list)
    csv_row.append(numpy.float64(sum(list))/size)
    csv_row.append(list[int(len(list)/2)])
    csv_row.append(list[0])
    csv_row.append(list[-1])

def extract_tweet_metrics(tweet_list):
    global csv_row
    total_string = ""
    hashtag_count_array = []
    hashtag_per_word_array = []
    url_count_array = []
    url_per_word_array = []
    tweet_size_array = []
    mention_count_array = []
    numeric_characters_count_array = []
    word_count_array = []
    retweet_count_array = []
    total_string = ""
    for tweet in tweet_list:
        try:
            total_string += " " + tweet["text"]
            word_count = len(re.findall(r"\w+", tweet["text"]))
            url_count = len(re.findall(r"((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", tweet["text"]))
            hashtag_count = len(re.findall(r"#\w+", tweet["text"]))
            tweet_size_array.append(len(tweet["text"]))
            hashtag_per_word_array.append(numpy.float64(hashtag_count)/word_count)
            hashtag_count_array.append(hashtag_count)
            url_per_word_array.append(numpy.float64(url_count)/word_count)
            url_count_array.append(url_count)
            mention_count_array.append(len(re.findall(r"@\w+", tweet["text"])))
            numeric_characters_count_array.append(len(re.findall(r"\d", tweet["text"])))
            word_count_array.append(word_count)
            retweet_count_array.append(len(re.findall(r"RT\s*@\w+", tweet["text"])))
        except Exception, ex:
            print "The tweet text is " + tweet["text"]
            raise

    insert_into_csv(hashtag_per_word_array)
    insert_into_csv(url_per_word_array)
    insert_into_csv(tweet_size_array)
    insert_into_csv(hashtag_count_array)
    insert_into_csv(mention_count_array)
    insert_into_csv(numeric_characters_count_array)
    insert_into_csv(url_count_array)
    insert_into_csv(word_count_array)
    insert_into_csv(retweet_count_array)    

def extract_tweet_timing_metrics(tweet_list):
    global csv_row
    if (len(tweet_list) == 0):
        insert_into_csv(tweet_list)
        insert_into_csv(tweet_list)
        insert_into_csv(tweet_list)
        return

    intertweet_time_array = []
    daily_tweet_counts = []
    weekly_tweet_counts = []
    daily_tweet_count = 0
    weekly_tweet_count = 0
    start_date = parser.parse(str(tweet_list[0]["created_at"])).date()
    for index, tweet  in enumerate(tweet_list):
        time_first = parser.parse(str(tweet["created_at"]))
        if index < len(tweet_list) - 1:
            time_next = parser.parse(str(tweet_list[index+1]["created_at"]))
            intertweet_time_array.append((time_first - time_next).seconds)
        if (time_first.date() == start_date): #same day, and hence same week
            daily_tweet_count += 1
            weekly_tweet_count += 1
        else:
            daily_tweet_counts.append(daily_tweet_count)
            daily_tweet_count = 1
            if (((start_date - time_first.date()).days > 7) or (time_first.weekday() > start_date.weekday())):
                weekly_tweet_counts.append(weekly_tweet_count)
                weekly_tweet_count = 1
            else:
                weekly_tweet_count += 1
            start_date = time_first.date()

    daily_tweet_counts.append(daily_tweet_count)
    weekly_tweet_counts.append(weekly_tweet_count)

    time_first = parser.parse(str(tweet_list[0]["created_at"]))
    time_last = parser.parse(str(tweet_list[-1]["created_at"]))
    day_count = (time_first - time_last).days
    insert_into_csv(intertweet_time_array)
    insert_into_csv(daily_tweet_counts, day_count)
    insert_into_csv(weekly_tweet_counts, round(numpy.float64(day_count)/7))


def retrieve_tweets(user_id, directory):
    global csv_row
    tweet_file = open(directory + 'tweets.json', 'w')
    page_no = 1
    tweet_list = list()
    while page_no <= 16:
        tweets = json.loads(api_raw.user_timeline(id=user_id, page=page_no, count=200, include_rts=True))
        if tweets:
            for tweet in tweets:
                tweet_list.append(tweet)
        else:
            break
        page_no += 1
    url_count = 0
    reply_count = 0
    for tweet in tweet_list:
        tweet_file.write(json.dumps(tweet) + '\n')
        try:
            if (re.search(r"((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", tweet["text"])):
                url_count += 1
            if (tweet["in_reply_to_status_id_str"]):
                reply_count += 1
        except:
            print tweet["text"]
    csv_row.append(numpy.float64(reply_count)/len(tweet_list))
    csv_row.append(numpy.float64(url_count)/len(tweet_list))
    csv_row.append(reply_count)
    extract_tweet_metrics(tweet_list)
    tweet_file.close()
    return tweet_list

def get_friend_list(friends):
    friend_names = open("follower_names.txt", 'w')
    friend_ids = open("follower_ids.txt", 'w')
    for friend in friends:
        # print friend.id
        friend_ids.write(str(friend.id) + '\n')
        friend_names.write(friend.screen_name + '\n')
    friend_ids.close()
    friend_names.close()

def retrieve_friends_followers_and_mentions(user_id, directory):
    global csv_row
    print "before"
    print_rate_limits()
    # followers = tweepy.Cursor(api.followers, user_id=user_id, count=200).items()
    # get_friend_list(followers)
    friends = tweepy.Cursor(api.friends, user_id=user_id, count=200).items()
    mentions = tweepy.Cursor(api.mentions_timeline, user_id=user_id, count=200).items()
    print "after"
    print_rate_limits()
    write_peer_info(friends, directory + "friends.json")
    write_peer_info(mentions, directory + "mentions.json")

    mention_count = 0 
    reply_count = 0 
    for mention in mentions:
        mention_count += 1
        if(mention.in_reply_to_status_id_str):
            reply_count += 1

    # get_friend_list(friends)
    # return
    # csv_row.append(sum([follower.friends_count for follower in followers]))
    csv_row.extend((mention_count, reply_count))
    csv_row.append(sum([friend.statuses_count for friend in friends]))

def insert_user_info(user_info):
    global csv_row
    csv_row.append(user_info["friends_count"])
    csv_row.append(user_info["followers_count"])
    csv_row.append(user_info["statuses_count"])

def extract_user_info(users_info):
    global csv_row
    data = []
    fp = open('spammer-result.csv', 'w')
    writer = csv.writer(fp, delimiter=',')
    try:
        for user_info in users_info:
            try:
                print "user_id is " + str(user_info["id"])
                print "user_name is " + str(user_info["screen_name"])
                csv_row = []
                if (user_info["friends_count"] > 2900):
                    print "too many friends to pull"
                    continue
                if (user_info["protected"] == True):
                    print "user is protected"
                    continue
                # pickled = jsonpickle.encode(user_info)
                # user_json_object = json.loads(pickled)
                csv_row = [numpy.float64(user_info["followers_count"])/user_info["friends_count"]] #initializing the csv with the first feature
                user_json_string = json.dumps(user_info, indent=4, sort_keys=True)
                user_id = user_info["id"]
                directory = "data_collected/" + str(user_id) + "/"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                else:
                    continue
                tweet_list = retrieve_tweets(user_id, directory) #extracts 36 features
                insert_user_info(user_info) #3 more features
                retrieve_friends_followers_and_mentions(user_id, directory)
                extract_tweet_timing_metrics(tweet_list)
                user_details = open(directory + 'user.json','w')
                user_details.write(user_json_string)
                user_details.close()
                csv_row.append(user_info["screen_name"])
                csv_row.append(user_info["id"])
                # data.append(csv_row)
                writer.writerow(csv_row)
            except Exception, ex:
                shutil.rmtree(directory)
                logging.exception("Exception happened!")
                fp.close()
                raise
    finally:
        fp.close()

def chunks(l, n): #Yield successive n-sized chunks from l.
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def get_user_ids_from_trends():
    users_ids = ""
    for json_line in open("trends.json"):
        if (json_line == '\n'):
            continue
        id = str(json.loads(json_line)["user"]["id"])
        if id not in users_ids:
            users_ids += id + "\n"
    random = open("anonymous.txt", "w")
    random.write(users_ids)
    random.close()
    exit

def read_file_into_array():
    return [int(name.strip()) for name in open('spammer_ids.txt')]

def get_user_features_for_non_spammers():
    screen_names = read_file_into_array()
    chunked_names = chunks(screen_names, 99)
    for id_set in chunked_names:
        users_info = json.loads(api_raw.lookup_users(user_ids=id_set))
        extract_user_info(users_info)

def get_user_ids_from_user_names():
    screen_names = [name.strip() for name in open('flat_spammer_list.txt')]
    # return
    # for name_list in chunked_names:
    users = json.loads(api_raw.lookup_users(screen_names=screen_names))
    user_ids = [str(user['id']) for user in users]
    # user_names = [user['screen_name'] for user in users]
    user_file = open("spammer_ids.txt", "w")
    user_file.write("\n".join(user_ids))
    user_file.close()
    exit

index = 0
while True:
    try:
        print "Trying auth " + str(index)
        auth = get_auth(index)
        api_raw = tweepy.API(auth, parser=RawJsonParser())
        api = tweepy.API(auth)

        # get_user_features_for_non_spammers()
        get_user_ids_from_user_names()
        # get_user_ids_from_trends()
        # break
    except tweepy.TweepError:
        print "Rate limit exceeded. Moving on to next appln"
        index += 1
        if (index == 4):
            print "sleeping for 15 minutes"
            time.sleep(60 * 15)
        index %= 4
    except Exception, ex:
        logging.exception("Something awful happened!")
        print ex

# print_rate_limits()
# extract_user_info([json.loads(api_raw.get_user(screen_name='littlecegian07'))])