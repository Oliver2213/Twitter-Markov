#Markov chaining twitter bot
#Author: Blake Oliver <oliver22213@me.com>

import markov
import tweepy
import bot
from keys import * #import our user keys

#Twitter auth stuff
auth = tweepy.OAuthHandler(c_key, c_secret) 
auth.set_access_token(token, token_secret)
api = tweepy.API(auth) # Get our API object


def main():

    try:
        me = api.me()
        print "Starting userstream for %s ( %s )" %(me.name, me.screen_name)
        mybot = bot.Bot(api)
        stream = tweepy.Stream(auth, bot.BotStreamListener(api, mybot))
        #Start the stream
        stream.userstream()

    except KeyboardInterrupt:
        mybot.cleanup()
        print('goodbye!')

if __name__ == '__main__':
    main    ()