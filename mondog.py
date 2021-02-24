import requests
from datetime import date
import random
import os
from dogbot import get_gif

def main():
    if date.today().weekday() == 0:
        DOGS_CHANNEL =  os.getenv("DOGS_CHANNEL")
        gif_URL = get_gif()
        slack_payload = {
            "blocks": [
                {
                    "type": "image",
                    "image_url": gif_URL,
                    "alt_text": "dog",
                    "title": {
                        "type": "plain_text",
                        "text": "Happy Mondog!"
                    }
                }
            ]
        }
        
        r = requests.post("https://hooks.slack.com/services/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", json=slack_payload)
        print(r.status_code)
        return

if __name__ == "__main__":
    main()