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
    default_doggy = "https://media1.giphy.com/media/4Zo41lhzKt6iZ8xff9/giphy-downsized.gif?cid=5a8f66bfo4oi0rpi1ldikr8dknqdcfwlndpf7pbkvyptl1ud&rid=giphy-downsized.gif"
    try:
        gif_URL = giphy_response.get('data', default_doggy)[0].get('images', default_doggy).get('downsized', default_doggy).get('url', default_doggy)
    except AttributeError:
        gif_URL = default_doggy

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
    url =data['response_url']
    print(url)
    slack_request = requests.post(url, json=slack_payload, headers={"Content-type": 'application/json'})
    return ("", 200)
