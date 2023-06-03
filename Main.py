import os
import requests
import time
from dotenv import load_dotenv

load_dotenv("./secret/secret.env")

def download_images(api_key, tag, number_of_images):
    url = "https://konachan.com/post.json"
    headers = {
        "User-Agent": "MyApp/1.0",
    }

    params = {
        "tags": tag,
        "limit": number_of_images,
        "api_key": api_key,
    }

    response = requests.get(url, headers=headers, params=params)
    posts = response.json()

    if response.status_code == 200:
        os.makedirs('images', exist_ok=True) # This line creates a new directory named 'images' if it does not exist already
        for post in posts:
            img_url = post["file_url"]
            img_data = requests.get(img_url).content
            with open(os.path.join('images', os.path.basename(img_url)), 'wb') as handler:
                handler.write(img_data)
            time.sleep(1)
    elif response.status_code == 421:
        print("User is throttled, try again later")
    else:
        print(f"Failed to get posts, status code: {response.status_code}")

api_key = os.getenv("API_KEY")
tag = "cat_ears"
number_of_images = 10

download_images(api_key, tag, number_of_images)
