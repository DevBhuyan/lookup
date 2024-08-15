#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 01:47:13 2024

@author: dev
"""

from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
import os

os.makedirs('./query_files', exist_ok=True)


def google_this(query: str = "hi"):
    src = "https://www.google.com/search?"
    payload = {
        "q": query,
        "sourceid": "chrome",
        "ie": "UTF-8"
    }
    encoded_params = urlencode(payload)

    response = requests.get(src + encoded_params)

    with open(f'./query_files/{query}.html', 'w') as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')

    urls = []
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/url'):
            urls.append(a['href'])

    return urls


if __name__ == "__main__":

    urls = google_this()

    context = []
    for idx, url in tqdm(enumerate(urls), total=len(urls)):
        try:
            response = requests.get('https://www.google.com' + url)
            text = BeautifulSoup(response.text, 'html.parser').get_text()
            context.append(text.replace("\n\n", "\n").replace(
                "\n\n", "\n").replace("\n\n", "\n").replace("\n\n", "\n"))
        except:
            pass
    context = "\n\n".join(context)
