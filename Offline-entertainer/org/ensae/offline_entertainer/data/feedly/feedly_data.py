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

user_categories = list(itertools.combinations(feedly.get_categories(), 2))
user_id_start = 3
user_id = user_id_start

pocket_like_articles={}
for categories in user_categories :
    user_articles = {}
    for category in categories:
        articles = feedly.get_engaging_content(category['id'], count=1000)
        for article in articles['items']:
            has_image = (article.get('visual') != None)
            try :
                text = strip_tags(article['summary']['content'])
            except KeyError as e :
                print(e)
                print(article)
            pocket_like = PocketResource(article['fingerprint'], article['alternate'][0]['href'], True, None, has_image,
                                         article['title'], text, time_added=(article['published']/1000),
                                         language=TextLearning.detect_language(article['title']),category=category['label'])
            user_articles[article['fingerprint']]=pocket_like
    pocket_like_articles[str(user_id)] = user_articles
    user_id = user_id +1
with open('pocket_like_data.json', 'w') as f:
    json.dump(pocket_like_articles, f, default=PocketResource.obj_dict)


def wait():
    msvcrt.getch()
