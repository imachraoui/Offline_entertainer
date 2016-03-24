import json
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource
from org.ensae.offline_entertainer.server.learning.TextLearning import TextLearning
from org.ensae.offline_entertainer.server.learning.rss.RSSFeedsHelper import *
import datetime
import urllib3
from collections import Counter
import operator
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
import pandas
import numpy as np

# Get all user ids available in DB
def get_users(file_path):
    with open(file_path, 'r') as f_pocket:
        articles = json.load(f_pocket)
        userids = list(articles.keys())
    return(userids)

# Get all user's articles available in DB
def get_all_user_articles(userid,language=None):
    pocket_articles = get_articles(userid,'../data/pocket/pocket_formatted_data.json',language)
    return(pocket_articles)

def get_articles(userid,path_to_file,language=None) :
    with open(path_to_file, 'r') as f:
        articles = json.load(f)
        articles_per_user= []
        o = json.dumps(articles[userid])
        articles_for_user = json.loads(o)
        for b in articles_for_user :
            if articles_for_user[b].get("language")==None :
                articles_for_user[b]["language"] = 'french'
            if (language == None) | (articles_for_user[b]["language"] == language ) :
                articles_per_user.append(articles_for_user[b])
    return(articles_per_user)

# Add an article to user's DB based upon its URL
def add_article(url,pocket_client,userid):
    if pocket_client.access_token == None :
        try:
            pocket_client.authorize2()
        except TypeError as e:
            print(e)
            raise
    current_timestamp= datetime.datetime.now().timestamp() -1000
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
    # Take only 2 of each listed domains
    domains = TextLearning.get_weighted_domains(get_all_user_articles(userid))
    domains = [x[0] for x in domains][0:2]
    indexed_domains = get_indexed_domains()

    a_o_i = TextLearning.get_areas_of_interest(userid)
    a_o_i = [x[0] for x in a_o_i]
    for area in a_o_i[0:2] :
        sites = indexed_domains[area]
        # pick 1 site randomly from the list
        domains.append(sites[np.random.choice(len(sites),1)])

    recommendations = []
    for domain in domains :
        recommendations.extend(get_rss_feeds(domain,2))

    return(recommendations)

def compute_recommendation_model():

    base_file = "../data/feedly/pocket_like_data.json"
    user_ids = get_users(base_file)
    tuple_texts_categories=[]

    for user_id in user_ids :
        tuple_texts_categories.extend(TextLearning('english').get_stemmed_texts(user_id,base_file,True))

    texts= [x[0] for x in tuple_texts_categories]
    categories= [x[1] for x in tuple_texts_categories]
    for_df = {"texts" : texts, "categories":categories}
    data = pandas.DataFrame(for_df,columns=["texts","categories"])

    # Split into 2 data sets, one for training the other for test
    train,test = train_test_split(data, train_size=0.5)
    text_vectorizer = CountVectorizer(analyzer='word')
    train_matrix= text_vectorizer.fit_transform(train['texts'])
    test_matrix= text_vectorizer.transform(test['texts'])

    classifier = MultinomialNB().fit(train_matrix,train['categories'])
    print(classifier.score(test_matrix,test["categories"]))

    TextLearning.text_vectorizer = text_vectorizer
    TextLearning.recommendation_model = classifier

def get_indexed_domains():
    with open('../data/feedly/pocket_like_data_sites.json', 'r') as f:
        sites= json.load(f)
    return(sites)


