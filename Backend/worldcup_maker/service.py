import openai
import os
import requests
from dotenv import load_dotenv
import re

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=env_path)
openai_api_key = os.getenv('gptApiKey')
client = openai.OpenAI(api_key=openai_api_key)

def get_top_image_urls(queries):
    api_key = os.getenv('googleSearchKey')
    cse_id = os.getenv('googleCSEId')

    result = []

    for query in queries:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cse_id}&key={api_key}&searchType=image&num=1"
        response = requests.get(url)
        data = response.json()
        print(data)
        if 'items' in data and len(data['items']) > 0:
            image_url = data['items'][0]['link']
            result.append((query, image_url))
        else:
            result.append((query, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQC0Mop6s6wJ2kNSKyAcHQRIjweaHlsr1Cv8CqijMIZBg&s"))

    return result

def generate_candidates(prompt, num_candidates):
    full_prompt = f"Create a list of {num_candidates} candidates for: {prompt}. Surround each candidate with <>. If the prompt is in Korean, generate candidates in Korean; if it is in English, generate candidates in English. Also, ensure the candidates are unique."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    candidates_text = response.choices[0].message.content
    return candidates_text

def extract_bracketed_strings(text):
    pattern = r'<(.*?)>'
    matches = re.findall(pattern, text)
    filtered_matches = [match for match in matches if match.strip()]
    return filtered_matches