import csv
import json
import os
import re
import time

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


def fetch_static_html_body_only(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove all <script> tags
    for script in soup.find_all("script"):
        script.decompose()

    # Extract only the <body> content
    body_content = soup.body

    return body_content.prettify() if body_content else ""


def save_as_file(txt: str, filename: str, is_step=False) -> str:
    path = f"output/{project}/{filename}"
    if is_step:
        os.makedirs(f"output/{project}/steps", exist_ok=True)
        path = f"output/{project}/steps/{filename}.txt"
    with open(path, "w") as f:
        f.write(txt)
    return "success"


def save_as_json_file(data: dict, filename: str, is_step=False) -> str:
    path = f"output/{project}/{filename}"
    if is_step:
        os.makedirs(f"output/{project}/steps", exist_ok=True)
        path = f"output/{project}/steps/{filename}.json"
    if not path.endswith(".json"):
        path += ".json"
    with open(path, "w") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    return "success"


def extract_json_from_string(input_string):
    json_pattern = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
    match = json_pattern.search(input_string)
    if match:
        json_str = match.group(1)
    else:
        json_str = input_string
        json_str = json_str.replace('\n', '').strip()
        while not json_str.startswith('{'):
            json_str = json_str[1:]
        while not json_str.endswith('}'):
            json_str = json_str[:-1]
    try:
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return ""

def save_urls_as_images(list_urls, folder_name):
    os.makedirs(f"output/{project}/images/{folder_name}", exist_ok=True)
    for u in list_urls:
        time.sleep(0.2)
        response = requests.get(u)
        with open(
            f"output/{project}/images/{folder_name}/{u.split('/')[-1]}", "wb"
        ) as f:
            f.write(response.content)
    return "success"


def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)
    return "success"


def open_file_as_string(filename: str) -> str:
    with open(f"output/{project}/{filename}", "r") as f:
        return f.read()


def extract_list_from_json(json_data):
    json_str = json.dumps(json_data)
    first_bracket = json_str.find('[')
    last_bracket = json_str.rfind(']')
    list_str = json_str[first_bracket:last_bracket+1]
    return json.loads(list_str)

def save_json_as_csv(data: dict, filename: str) -> str:
    path = f"output/{project}/{filename}"
    if not path.endswith(".csv"):
        path += ".csv"
    items = extract_list_from_json(data)
    # Ensure items is a list of dictionaries
    if not isinstance(items, list):
        raise ValueError(f"Invalid data format: {items}")
    # If items is a list of strings, convert it to a list of dictionaries
    if all(isinstance(item, str) for item in items):
        items = [{"value": item} for item in items]
    elif not all(isinstance(item, dict) for item in items):
        raise ValueError(f"Invalid data format: {items}")
    # Get the keys from the first dictionary in the list
    if items:
        keys = items[0].keys()
    else:
        keys = []  # Handle empty list case
    file_exists = os.path.isfile(path)
    
    # Write to the CSV file
    with open(path, "a" if file_exists else "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if not file_exists:
            writer.writeheader()
        writer.writerows(items)
    return "success"