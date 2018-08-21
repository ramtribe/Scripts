
#!/usr/bin/python

import os
import flask 
import requests
from slackclient import SlackClient

##client_id = ''
##client_secret = ''
slack_token_oauth_bot = 'xoxb-75582660320-402640456882-vrq7wB5sU8mgo1mb5FTFHvs1'
sc = SlackClient(slack_token_oauth_bot)

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistant memory store.
authed_teams = {}

sc.api_call(
    "chat.postMessage",
    channel = "bot_test",
    text = "knock! knock!"
    )

