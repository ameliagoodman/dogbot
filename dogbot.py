import requests
import random
import os
from flask import Flask, request
app = Flask(__name__)

def get_gif():
    API_KEY =  os.getenv("GIPHY")
    

    giphy_payload = {'api_key': API_KEY, 'q': 'dog', 'limit': 1, 'offset': random.randint(0, 1000), 'rating': 'g'}
    giphy_request = requests.get('http://api.giphy.com/v1/gifs/search', params=giphy_payload)
    giphy_response = giphy_request.json()
    gif_URL = giphy_response.get('data', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9')[0].get('images', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9').get('downsized', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9').get('url', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9')
    return gif_URL

@app.route('/', methods=['GET', 'POST'])
def main():
    return "Hello dog"

@app.route('/fetch', methods=['GET', 'POST'])
def hello_dog():
    SLACK_URL =  os.getenv("SLACK_URL")
    data = request.form
    
    gif_URL = get_gif()
    slack_payload = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "image",
                "image_url": gif_URL,
                "alt_text": "dog",
                "title": {
                    "type": "plain_text",
                    "text": "arf!"
                }
            }
        ]
    }
    url = SLACK_URL + data['channel_id']
    print(url)
    slack_request = requests.post(url, json=slack_payload, headers={"Content-type": 'application/json'})
    return "arf"

