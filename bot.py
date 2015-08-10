#This file contains the bot's classes and methods

import tweepy
import tempfile

class Bot(object):
    """
Handles spesific functions of the bot.
Flow:
Class should be instantiated with twitter API object
methods:
extract_mentions pulls all twitter handles out of the entities sent along with a status update. The resulting list does not have the @ sign attached to each name, this is done in main.
extractTL pulls the latest 200 tweets from the provided user's timeline and tosses their text into a temp file, then returns that file path and name
Main can then use that file name with the markov library to generate a markov dict and pull a response out of it


"""
    def __init__(self, twitterAPI):
        """
This method initializes the bot class with the twitter API in use, other methods use this value, so when instantiating this class be sure to do it like:
bot = bot.bot(api)
then other methods can be accessed and they'll use the right api object
"""
        self.twitterAPI = twitterAPI

    def extract_mentions(self, tweet):
        """Return a list of @mentionnames in the provided tweet object"""
        self.tweet = tweet
        self.mentionnames = []
        for item in self.tweet.entities['user_mentions']:
            self.mentionnames.append(self.tweet.entities['user_mentions'][item]['screen_name'])
        return self.mentionnames

    def extractTL(self, userid):
        """Takes a user's timeline and extracts the text of each tweet into a temp file, then returns the path and name to that file"""
        self.userid = userid
        self.tempfile = tempfile.NamedTemporaryFile(prefix=str(self.userid), suffix='.tmp', delete=False)
        self.temptl = self.twitterAPI.user_timeline(self.userid, count=200)
        #Gotta be a better way of doing this...
        self.num=0
        for item in self.temptl:
            self.tweettext = self.temptl[self.num].text
            self.tweettext = self.tweettext+"\n"
            self.tempfile.write(tweettext)
            self.num = self.num+1
        self.tempfile.flush()


class BotStreamListener(tweepy.StreamListener):
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

