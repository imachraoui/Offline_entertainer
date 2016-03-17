import json
import sys
import os
from flask import Flask, Response, request
from org.ensae.offline_entertainer.data.pocket import articles_service
from org.ensae.offline_entertainer.data.pocket.PocketApi import PocketApi
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

CONSUMER_KEY = "51103-6fabe37f547915c157c02f7b"
REDIRECT_URI = "http://localhost:3000/index.html?user_id="

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
    except :
        print("Unexpected error:", sys.exc_info())
        raise

    return Response(json.dumps(articles), mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

@app.route('/api/addArticle', methods=['POST'])
def addComment_handler():
    article = articles_service.add_article(request.form['url'],client_pocket,request.form['user_id'])
    result=[]
    result.append(article[list(article.keys())[0]])
    return Response(json.dumps(result, default=PocketResource.obj_dict), mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

@app.route('/api/auth', methods=['GET'])
def auth():
    try :
        redirect_url = client_pocket.authorize(REDIRECT_URI)
        return Response(redirect_url, headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    except TypeError as e :
        print(e)
        raise

@app.route('/api/users', methods=['GET'])
def getUsers():
    try :
        userids = articles_service.get_users()
        return Response(json.dumps(userids),  mimetype='application/json',headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    except TypeError as e :
        print(e)
        raise

@app.route('/api/recommendations/<userid>', methods=['GET'])
def getRecommendations(userid):
    try :
        recos = articles_service.get_recommendations(userid)
        print(recos)
        return Response(json.dumps(recos),  mimetype='application/json',headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    except TypeError as e :
        print(e)
        raise


# Launch Flask server
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT",3000)))

