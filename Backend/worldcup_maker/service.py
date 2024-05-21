import os
import requests
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=env_path)

def get_top_image_urls(queries):
    api_key = os.getenv('googleSearchKey')
    cse_id = os.getenv('googleCSEId')

    result = []

    for query in queries:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cse_id}&key={api_key}&searchType=image&num=1"
        response = requests.get(url)
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            image_url = data['items'][0]['link']
            result.append((query, image_url))
        else:
            result.append((query, None))

    return result

