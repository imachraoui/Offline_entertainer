import ssl
import urllib
import urllib3.request as req
import urllib3.response as resp
from flask import redirect
import requests

class PocketApi():

    def __init__(self,consumer_key,redirect_uri):
        self.context = ssl._create_unverified_context()
        self.consumer_key = consumer_key
        self.redirect_uri = redirect_uri
        self.auth()
        self.access_token = None
        #self.access_token = self.authorize(self.redirect_uri,self.request_token)

    def auth(self):
        values ={'consumer_key' : self.consumer_key,'redirect_uri' : self.redirect_uri}
        data= self.parse_input(values)
        response = urllib.request.urlopen("https://getpocket.com/v3/oauth/request", data=data, context=self.context)
        responseText = response.readall()
        self.request_token = responseText.decode('ascii').rsplit('=')[1]

    def parse_input(self,values) :
        data = req.urlencode(values)
        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        return(data)

    def authorize(self,redirect_uri):
        values ={'redirect_uri' : redirect_uri,'request_token' : self.request_token}
        data = self.parse_input(values)
        response = urllib.request.urlopen("https://getpocket.com/auth/authorize", data=data, context=self.context)
        # Step 2 : Access to URL
        url = 'https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=%s' % (self.request_token, urllib.parse.quote(redirect_uri))
        return (url)
        #input("Copy-Paste the url then press Enter when finished ....")
        print(requests.post(url))

    def authorize2(self):
        # Step : Final authorization
        values ={'consumer_key' : self.consumer_key,'code' : self.request_token}
        data = self.parse_input(values)
        response = urllib.request.urlopen("https://getpocket.com/v3/oauth/authorize", data=data, context=self.context)
        responseText = response.readall()
        self.access_token = responseText.decode('ascii').rsplit('=')[1].rsplit('&')[0]

    def get(self,since=None):
        values ={'consumer_key' : self.consumer_key,'access_token' :self.access_token,'state':'all'}
        if since != None :
            values.update({"since":since})
        data = self.parse_input(values)
        response = urllib.request.urlopen("https://getpocket.com/v3/get", data=data, context=self.context)
        responseread = response.readall()
        return(responseread.decode('ascii'))

    def add_content(self, url):
        values ={'url':url,'consumer_key' : self.consumer_key,'access_token' :self.access_token}
        data = self.parse_input(values)
        response = urllib.request.urlopen("https://getpocket.com/v3/add", data=data, context=self.context)
        responseread = response.readall()
        return(responseread.decode('ascii'))


