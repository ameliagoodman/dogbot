import requests
import random
import os
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    return "Hello dog"

@app.route('/fetch', methods=['GET', 'POST'])
def hello_dog():
    API_KEY =  os.getenv("GIPHY")
    SLACK_URL =  os.getenv("SLACK_URL")
    data = request.headers
    giphy_payload = {'api_key': API_KEY, 'q': 'dog', 'limit': 1, 'offset': random.randint(0, 1000), 'rating': 'g'}
    giphy_request = requests.get('http://api.giphy.com/v1/gifs/search', params=giphy_payload)
    giphy_response = giphy_request.json()
    gif_URL = giphy_response.get('data', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9')[0].get('images', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9').get('downsized', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9').get('url', 'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9')

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
            }, 
            # {
            #     "type": "actions",
            #     "block_id": "newdog?",
            #     "elements": [
            #         {
            #             "type": "button",
            #             "text": {
            #                 "type": "plain_text",
            #                 "text": "good dog"
            #             },
            #             "style": "primary",
            #             "action_id": "send_dog",
            #         },
            #         {
            #             "type": "button",
            #             "text": {
            #                 "type": "plain_text",
            #                 "text": "grrr"
            #             },
            #             "style": "danger",
            #             "action_id": "new_dog",
            #         }
            #     ]
                
            # }
        ]
    }
    print(data)
    slack_request = requests.post(SLACK_URL, json=slack_payload)
    return 'Hello, Dog!'

