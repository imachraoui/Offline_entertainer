import json
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource
import datetime


with open('./pocket_test.json', 'r') as f:
    test = json.load(f)

with open('./pocket_formatted_data.json', 'w+') as f:
    for userid in test:
        f.write('\n')
        o = json.dumps(test[userid])

        b = json.loads(o, object_hook=PocketResource.as_pocketresource)
        newresource = PocketResource(uid='123456',has_image=1, url='httptest', is_article=1, has_video=0,
                                     title='titre de l\'article',
                                     text="Ceci est le texte de l'article",time_added=datetime.datetime.now().time())
        b.update({'1': newresource})
        test[userid] = b
        json.dumps(test, default=PocketResource.obj_dict)
    json.dump(test, f, default=PocketResource.obj_dict)
