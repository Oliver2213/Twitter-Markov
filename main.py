#Markov chaining twitter bot
#Author: Blake Oliver <oliver22213@me.com>

import bot
import markov
import tweepy
from keys import * #import our user keys

#Twitter auth stuff
auth = tweepy.OAuthHandler(c_key, c_secret) 
auth.set_access_token(token, token_secret)
api = tweepy.API(auth) # Get our API object


def main():

    try:
        me = api.me()
        print "Starting userstream for %s ( %s )" %(me.name, me.screen_name)
        stream = tweepy.Stream(auth, bot.BotStreamListener())
        #Start the stream
        stream.userstream()

    except KeyboardInterrupt:
        print('goodbye!')

if __name__ == '__main__':
    main    ()