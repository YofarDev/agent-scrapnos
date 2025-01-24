import json
import os
import re

import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

project = ""




def fetch_dynamic_content_with_playwright(url: str) -> str:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # headless=False opens a visible browser
        context = browser.new_context(user_agent=ua)
        page = context.new_page()
        page.goto(url)
        # Wait for the page to load
        page.wait_for_timeout(2123)
        content = page.locator("body").inner_text()
        browser.close()
        return content


def fetch_static_html_with_requests(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.prettify()


def save_as_txt_file(txt: str, filename: str) -> str:
    with open(f"output/{project}/{filename}", "w") as f:
        f.write(txt)
    return "success"





def save_as_json_file(data: dict, filename: str) -> str:
    with open(f"output/{project}/{filename}.json", "w") as f:
        f.write(json.dumps(data))
    return "success"



def extract_json_from_string(input_string):
    json_pattern = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
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
    os.makedirs("output", exist_ok=True)
    os.makedirs(folder_name, exist_ok=True)
    for u in list_urls:
        response = requests.get(u)
        with open(f"output/{project}/{folder_name}/{u.split('/')[-1]}", "wb") as f:
            f.write(response.content)
    return "success"


def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    return "success"

def open_file_as_string(filename: str) -> str:
    with open(f"output/{project}/{filename}", "r") as f:
        return f.read()