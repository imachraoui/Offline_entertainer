
import json
import os
import time
from flask import Flask, Response, request
import sys
from org.ensae.offline_entertainer.data.pocket import articles_service
from org.ensae.offline_entertainer.data.pocket.PocketApi import PocketApi


app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
CONSUMER_KEY = "51103-6fabe37f547915c157c02f7b"
REDIRECT_URI = "http://localhost:3000"

try :
    client_pocket  = PocketApi(consumer_key=CONSUMER_KEY,redirect_uri=REDIRECT_URI)

except TypeError as e :
    print(e)
    raise

@app.route('/api/articles/<userid>', methods=['GET', 'POST'])
def display_articles(userid):

    try :
        articles = articles_service.get_articles(userid)
        print(articles)
    except TypeError as e :
        print(e)
        raise

    return Response(json.dumps(articles), mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

@app.route('/api/addArticle', methods=['POST'])
def addComment_handler():
    article = articles_service.add_article(request.form['url'],client_pocket,request.form['user_id'])

    return Response(article, mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

@app.route('/api/auth', methods=['GET'])
def auth():
    print(REDIRECT_URI)
    try :
        redirect_url = client_pocket.authorize(REDIRECT_URI)
        return Response(redirect_url, headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    except TypeError as e :
        print(e)
        raise

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT",3000)))
