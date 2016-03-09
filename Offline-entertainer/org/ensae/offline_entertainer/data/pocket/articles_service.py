import json
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource
from org.ensae.offline_entertainer.server.learning.TextLearning import TextLearning
import datetime

import urllib3
from collections import Counter
import operator

def get_users():
    with open('../data/pocket/pocket_formatted_data.json', 'r') as f:
        articles = json.load(f)
        userids = list(articles.keys())
        return(userids)

def get_articles(userid) :
 #   with open('pocket_formatted_data.json', 'r') as f:
    with open('../data/pocket/pocket_formatted_data.json', 'r') as f:
        articles = json.load(f)
        articles_per_user= []
    #    articles_per_user = {}
        o = json.dumps(articles[userid])
        articles_for_user = json.loads(o)
        for b in articles_for_user :
            articles_per_user.append(articles_for_user[b])
          #  articles_per_user[articles_for_user[b]["time_added"]] = articles_for_user[b]
        #articles_per_user.sort(key=lambda x: x["time_added"], reverse=True)
    return(articles_per_user)

def add_article(url,pocket_client,userid):
    if pocket_client.access_token == None :
        try:
            pocket_client.authorize2()
        except TypeError as e:
            print(e)
            raise
    current_timestamp= datetime.datetime.now().timestamp() -100
    response = pocket_client.add_content(url)
    response_formatted = json.loads(response)["item"]
    new_article = pocket_client.get(current_timestamp)
    new_article = json.dumps(json.loads(new_article)["list"])
    with open('../data/pocket/pocket_formatted_data.json', 'r') as f:
        allArticles= json.load(f)

    articles = json.loads(json.dumps(allArticles[userid]), object_hook=PocketResource.as_pocketresource_local)
    responseToObject = json.loads(new_article, object_hook=PocketResource.as_pocketresource)
    for key in responseToObject :
        responseToObject[key].language = TextLearning.detect_language(responseToObject[key].text)
    allArticles[userid].update(responseToObject)
    with open('../data/pocket/pocket_formatted_data.json', 'w') as f:
         json.dump(allArticles,f, default=PocketResource.obj_dict)
    return(responseToObject)

def get_recommendations(userid):
    domains = TextLearning.getDomains(userid)