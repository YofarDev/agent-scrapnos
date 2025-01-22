import json
import os
import re

import requests
from bs4 import BeautifulSoup


def extract_json_from_string(input_string):
    json_pattern = re.compile(r'```json\n(.*?)\n```', re.DOTALL)
    match = json_pattern.search(input_string)
    if match:
        json_str = match.group(1)
    else:
        json_str = input_string.strip()
    try:
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return ""



def save_urls_as_images(list_urls, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    for u in list_urls:
        response = requests.get(u)
        with open(f"{folder_name}/{u.split('/')[-1]}", "wb") as f:
            f.write(response.content)
    return "success"


def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    return "success"


def get_html_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.prettify()
