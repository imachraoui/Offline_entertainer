import feedly as f
import os
from flask import redirect
from org.ensae.offline_entertainer.data.feedly.FeedlyApi import FeedlyAPI
import msvcrt

FEEDLY_REDIRECT_URI = "https://sandbox.feedly.com"
FEEDLY_CLIENT_ID = "sandbox"
FEEDLY_CLIENT_SECRET = "JSSBD6FZT72058P51XEG"

feedly = FeedlyAPI(client_id=FEEDLY_CLIENT_ID, client_secret=FEEDLY_CLIENT_SECRET)
print(feedly.get_auth_url())
code = input("code -->...")

feedly.get_access_token(code)
feedly.get_categories()

def wait():
    msvcrt.getch()