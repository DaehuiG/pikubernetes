import openai
import os
import requests
import re

openai_api_key = os.getenv('gptApiKey')
client = openai.OpenAI(api_key=openai_api_key)

def get_top_image_urls(description, queries):
    api_key = os.getenv('googleSearchKey')
    cse_id = os.getenv('googleCSEId')
    result = []

    for query in queries:
        url = f"https://www.googleapis.com/customsearch/v1?q={description+" "+query}&cx={cse_id}&key={api_key}&searchType=image&num=1"
        response = requests.get(url)
        data = response.json()
        if 'items' in data and data['items']:
            image_url = data['items'][0]['link']
            result.append((query, image_url))
        else:
            result.append((query, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQC0Mop6s6wJ2kNSKyAcHQRIjweaHlsr1Cv8CqijMIZBg&s"))
    return result

def generate_candidates(prompt, num_candidates):
    full_prompt = f"Create a list of {num_candidates} candidates for: {prompt}. Surround each candidate with <>. If the prompt is in Korean, generate candidates in Korean; if it is in English, generate candidates in English. Also, ensure the candidates are unique. Also, please change {prompt} to a noun form and send it back within [ ]."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content

def extract_bracketed_strings(text):
    refined_description = [match for match in re.findall(r'\[(.*?)\]', text) if match.strip()][0]
    return refined_description, [match for match in re.findall(r'<(.*?)>', text) if match.strip()]

def compare_descriptions(input_description, all_descriptions):
    prompt = f"Compare the following description with the provided list and find those with the same meaning:\n\nInput Description:\n{input_description}\n\nList of Descriptions:\n"
    for id, description in all_descriptions:
        prompt += f"{id}: {description}\n"
    
    prompt += "\nReturn the IDs and descriptions of the entries that have the same meaning as the input description."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    result_text = response.choices[0].message.content
    same_meaning_descriptions = re.findall(r'(\d+): ([^\n]+)', result_text)
    return [(int(id), desc) for id, desc in same_meaning_descriptions]
