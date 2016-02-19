from bson import json_util
import datetime


class PocketResource(object):
    def __init__(self, uid, url, is_article, has_video, has_image, title, text, time_added=None, images=None,
                 videos=None):
        self.uid = uid
        self.url = url
        self.is_article = is_article
        self.has_video = has_video
        self.has_image = has_image
        if (time_added == None):
            time_added = datetime.datetime.now()
        else:
            self.time_added = time_added
        self.images = images
        self.videos = videos
        self.text = text
        self.title = title

    @staticmethod
    def as_pocketresource(dct):
        if 'resolved_url' in dct:
            return (
                PocketResource(dct['item_id'], dct['resolved_url'], dct['is_article'], dct['has_video'],
                               dct['has_image'],
                               dct['resolved_title'], dct['excerpt'],
                               dct['time_added']))
        else:
            return dct

    @staticmethod
    def as_pocketresource_local(dct):
        if 'url' in dct:
            return (
                PocketResource(dct['uid'], dct['url'], dct['is_article'], dct['has_video'], dct['has_image'],
                               dct['title'],
                               dct['text'],
                               dct['time_added']))
        else:
            return dct

    @staticmethod
    def obj_dict(obj):
        if isinstance(obj, datetime.time):
            # return (json_util.default(obj))
            return (obj.isoformat())
        return (obj.__dict__)
