import feedly as f
from org.ensae.offline_entertainer.data.feedly.FeedlyApi import FeedlyAPI
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource
from org.ensae.offline_entertainer.server.learning.TextLearning import TextLearning
from org.ensae.offline_entertainer.data.feedly.HTMLParser import *
import json
import msvcrt
import itertools

###############################################################
### Generate Data for Offline entertainer App from Feedly RSS Feeds
###############################################################

FEEDLY_REDIRECT_URI = "https://sandbox.feedly.com"
FEEDLY_CLIENT_ID = "sandbox"
FEEDLY_CLIENT_SECRET = "JSSBD6FZT72058P51XEG"

feedly = FeedlyAPI(client_id=FEEDLY_CLIENT_ID, client_secret=FEEDLY_CLIENT_SECRET)
print(feedly.get_auth_url())
code = input("code -->...")

feedly.get_access_token(code)

urls={}
for category in feedly.get_categories() :
            sites = []
            articles = feedly.get_engaging_content(category['id'], count=1000)
            for article in articles['items']:
                sites.append(article['origin']['htmlUrl'])
            urls[category['label']] = list(set(sites))
with open('pocket_like_data_sites.json', 'w') as f:
    json.dump(urls, f)


