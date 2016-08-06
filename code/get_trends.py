#encoding: UTF-8
import tweepy
import json

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="5PXRUCe0QNl2UXTlcIiYCA"
consumer_secret="p2FClXOwzO4yvAM2oAKcElRNk5WLsenJm73cFkTb4o"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="166457267-LVzoV1Y2W7y2aImys885YtYX4V1WY7YNkUzouYod"
access_token_secret="h4Qmc7UyLOTHeB25q6slF5LTw5cDxXSIz3nND5Xr906vn"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out

class StreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        print 'Ran on_status'

    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        return False

    def on_data(self, data):
        print data
        return True
        
stream_listener = StreamListener()
streamer = tweepy.Stream(auth=auth, listener=stream_listener)
setTerms = ['Thanksgiving', 'TellyExpressFaceOfTheYear', 'ThanksToStarWars', 'MomInspirations', 'tejpal', 'Jordan Hill', 'GarthBrooks']
response = json.dumps(streamer.filter(track = setTerms))