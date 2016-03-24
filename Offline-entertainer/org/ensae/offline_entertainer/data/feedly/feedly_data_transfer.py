import json
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource

with open('pocket_like_data.json','r') as f :
    feedly_articles = json.load(f)

with open('pocket_formatted_data.json','r') as f:
    pocket_articles = json.load(f)
with open('pocket_formatted_data.json','w') as f:
    pocket_articles.update(feedly_articles)
    json.dump(pocket_articles,f,default=PocketResource.obj_dict)