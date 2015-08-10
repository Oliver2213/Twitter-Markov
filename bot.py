#Markov chaining twitter bot
#Author: Blake Oliver <oliver22213@me.com>
import tweepy
import markov
from keys import * #import our user keys

#Twitter auth stuff
auth = tweepy.OAuthHandler(c_key, c_secret) 
auth.set_access_token(token, token_secret)
api = tweepy.API(auth) # Get our API object

class StdOutListener(tweepy.StreamListener):
    """Class that handles tweepy events.
E.g: on_connect, on_disconnect, on_status, on_direct_message, etc."""
    def on_connect( self ):
        print("Connection to twitter established!!")
        self.me = api.me()

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


def main():

    try:
        me = api.me()
        print "Starting userstream for %s ( %s )" %(me.name, me.screen_name)
        stream = tweepy.Stream(auth, StdOutListener())
        *Start the stream
        stream.userstream()

    except KeyboardInterrupt:
        print('goodbye!')

if __name__ == '__main__':
    main    ()