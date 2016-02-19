import json
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource
import datetime

def get_articles(userid) :
    with open('../data/pocket/pocket_formatted_data.json', 'r') as f:
        articles = json.load(f)
        a= []
        o = json.dumps(articles[userid])
        articles_for_user = json.loads(o)
        for b in articles_for_user :
            a.append(articles_for_user[b])

    return(a)

def add_article(url,pocket_client,userid):
    if pocket_client.access_token == None :
        try:
            pocket_client.authorize2()
        except TypeError as e:
            print(e)
            raise
    current_timestamp= datetime.datetime.now().timestamp()
    response = pocket_client.add_content(url)
    response_formatted = json.loads(response)["item"]
    content = pocket_client.get(current_timestamp)
    content = json.dumps(json.loads(content)["list"])
    with open('../data/pocket/pocket_formatted_data.json', 'r') as f:
        allArticles= json.load(f)

    articles = json.loads(json.dumps(allArticles[userid]), object_hook=PocketResource.as_pocketresource_local)
    responseToObject = json.loads(content, object_hook=PocketResource.as_pocketresource)
    allArticles[userid].update(responseToObject)
    with open('../data/pocket/pocket_formatted_data.json', 'w') as f:
         json.dump(allArticles,f, default=PocketResource.obj_dict)
    return(allArticles)

# response ='{"item":{"item_id":"1180591375","normal_url":"http:\/\/lesieur.fr\/Cuisine-populaire\/Sans-en-faire-tout-un-plat?utm_source=Outbrain&utm_medium=cpc&utm_campaign=web-serie-lesieur","resolved_id":"1180591375","extended_item_id":"1180591375","resolved_url":"http:\/\/www.lesieur.fr\/Cuisine-populaire\/Sans-en-faire-tout-un-plat?utm_source=Outbrain&utm_medium=cpc&utm_campaign=web-serie-lesieur","domain_id":"4101183","origin_domain_id":"4101183","response_code":"200","mime_type":"text\/html","content_length":"33699","encoding":"utf-8","date_resolved":"2016-02-01 03:59:48","date_published":"0000-00-00 00:00:00","title":"Sans en faire tout un plat avec Fred Chesneau","excerpt":"","word_count":"0","innerdomain_redirect":"1","login_required":"0","has_image":"0","has_video":"0","is_index":"0","is_article":"0","used_fallback":"0","lang":"fr","authors":[],"images":[],"videos":[],"resolved_normal_url":"http:\/\/lesieur.fr\/Cuisine-populaire\/Sans-en-faire-tout-un-plat?utm_source=Outbrain&utm_medium=cpc&utm_campaign=web-serie-lesieur","given_url":"http:\/\/www.lesieur.fr\/Cuisine-populaire\/Sans-en-faire-tout-un-plat?utm_source=Outbrain&utm_medium=cpc&utm_campaign=web-serie-lesieur"},"status":1}'
