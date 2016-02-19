from org.ensae.offline_entertainer.data.pocket.PocketApi import PocketApi
import json

CONSUMER_KEY = "51103-6fabe37f547915c157c02f7b"
REDIRECT_URI = "http://localhost:8080"

client_pocket  = PocketApi(consumer_key=CONSUMER_KEY,redirect_uri=REDIRECT_URI)
user_id=1
all_saved = client_pocket.get()

with open('C:/Users/wymeka/Documents/ENSAE/Projet-Python/pocket_data.json', 'w') as f:
    json.dump({user_id : all_saved},f)