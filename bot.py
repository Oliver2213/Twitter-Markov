#Markov chaining twitter bot
#Author: Blake Oliver <oliver22213@me.com>
import tweepy
import markov
from keys import * #import our user keys

#Twitter auth stuff
auth = tweepy.OAuthHandler(c_key, c_secret) 
auth.set_access_token(token, token_secret)
api = tweepy.API(auth) # Get our API object

class MarkovBot(object):
    """This class holds methods that make things much easier for the bot"""
    def __init__(self, twitterAPI, userid, include_profile=False):
        """
This method takes 3 args:
twitterAPI, which is the api object for this particular account. I almost always have this set to api, but no reason to be inflexible.
userid, which is a list with the Twitter user ID of the user or users mentioning the bot
include_profile, which is a boolean value that determines if the bot will include the user's profile description text in the markov chains file.
The method then calls the tweepy API method to get the last tweets of a user or users, parses that list, and dumps each tweet's text into a textfile.
"""
        self.twitterAPI = twitterAPI
        self.userid = userid
        self.include_profile = include_profile         




class StdOutListener(tweepy.StreamListener):
    """Class that handles tweepy streaming events.
E.g: on_connect, on_disconnect, on_status, on_direct_message, etc."""
    def on_connect( self ):
        """Gets run when the stream is first connected to twitter"""
        print("Connection to twitter established!!")
        self.me = api.me()

    def on_disconnect( self, notice ):
        """Gets run when the stream gets disconnected from twitter"""
        print("Connection to twitter lost!! : ", notice)

    def on_status( self, status ):
        """Gets run when the stream receives a status update (tweet)"""
        print(status.user.name+": \""+status.text+"\"")
        return True

    def on_direct_message(self, status):
        """Gets run when the stream receives a direct message"""
        print("Direct message received.")
        try:
            #If the DM isn't one that was sent from this account
            if status.direct_message['sender_screen_name'] != self.me.screen_name:
                print(status.direct_message['sender_screen_name']+": \""+status.direct_message['text']+"\"")
        except BaseException as e:
            print("Failed on_direct_message()", str(e))
        return True #Keep the stream open

    def on_error( self, status ):
        print(status)


def main():

    try:
        me = api.me()
        print "Starting userstream for %s ( %s )" %(me.name, me.screen_name)
        stream = tweepy.Stream(auth, StdOutListener())
        #Start the stream
        stream.userstream()

    except KeyboardInterrupt:
        print('goodbye!')

if __name__ == '__main__':
    main    ()