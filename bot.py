#This file contains the bot's classes and methods

import glob
import markov
from tweepy import StreamListener
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
This method initializes the bot class with the twitter API in use. Other methods use this value, so when instantiating this class be sure to do it like:
mybot = bot.bot(api)
then other methods can be accessed and they'll use the right api object
"""
        self.twitterAPI = twitterAPI
        self.mymarkov = markov.Markov(3, 140) #Instantiate an instance of the markov lib

    def extract_mentions(self, tweet):
        """Takes a standard tweepy tweet object, returns 2 lists: @mentionnames and IDs that correspond to those names, with the mentionname and ID of the account that is running the bot excluded"""
        self.tweet = tweet
        self.mentionnames = []
        self.mentionids = []
        for item in self.tweet.entities['user_mentions']:
            if item['screen_name'] != self.me.screen_name: #If this @mentionname doesn't belong to this account
                self.mentionnames.append(item['screen_name'])
            if item['id'] != self.me.id: #If the userID doesn't belong to this account
                self.mentionids.append(item['id'])
        return self.mentionnames, self.mentionids

    def extractTL(self, userids):
        """Takes iether a string with one id, or a list of multiple ones and extracts the text from all the tweets and dumps it into a text file, returning it's path"""
        self.userids = userids
        if isinstance(self.userids, str): #What's passed is probably just one ID
            self.temptl = self.twitterAPI.user_timeline(self.userids, count=200)
        elif isinstance(self.userids, list): # we have a list of IDs, iterate through
            self.temptl = [] #Create an empty list to add all our tweets to
            for item in self.userids:
                self.temptl.extend(twitterAPI.home_timeline(item, count=200)) #Append the tweets from what user ID we're on in the IDs list to the total list of tweets

        #Create a temporary file where all the extracted tweet text will go
        self.tempfile = tempfile.NamedTemporaryFile(prefix=str('twitter-markov-'), suffix='.tmp', delete=False)
        #Iterate through all the tweets in the list
        for item in self.temptl:
            #Pull out the text of the current tweet
            self.tweettext = item.text
            self.tweettext = self.tweettext+"\r\n" # add a newline char
            self.tempfile.write(self.tweettext) # Write our line containing the text of the tweet to the file
        self.tempfile.flush() # update the file on disk
        self.tempfile.close() # Close the file handle
        return self.tempfile.name # return the path to the textfile

    

    def cleanup(self):
        """Clean any temporary files the bot has created before shutdown"""
        self.tmpfilelist = glob.glob(tempfile.gettempdir()+'twitter-markov-[a-z0-9].tmp')
        self.removed=0
        for item in self.tmpfilelist:
            self.removed = self.removed+1
            os.remove(item)


class BotStreamListener(StreamListener):
    """Class that handles tweepy streaming events.
E.g: on_connect, on_disconnect, on_status, on_direct_message, etc.
"""

    def __init__(self, api, bot):
        # Adding a bot arg and code to store it in the instantiated class
        super(self.__class__, self).__init__(api)
        self.bot = bot

    def on_connect( self ):
        print("Connection to twitter established!!")
        self.me = self.api.me() #Store values about the authorized account


    def on_disconnect( self, notice ):
        print("Connection to twitter lost!! : ", notice)

    def on_status( self, status ):
        print(status.user.name+": \""+status.text+"\"")
        return True

    def on_direct_message(self, status):
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

