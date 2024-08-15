#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 01:39:53 2024

@author: dev
"""

import json
from streamlit import session_state as ss
import os
import streamlit as st


def load_message_history(last_n: int = 0,
                         sys_prompt: bool = True):

    file_path = f"./chains/{ss.session_code}_prompt_chain.json"

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            messages = list(json.load(f)['messages'])

        if not last_n:
            return messages
        else:
            try:
                MESSAGES = messages[-4:]
            except:
                MESSAGES = [messages[0], messages[2]]
            if sys_prompt:
                MESSAGES.insert(1, messages[1])

            return MESSAGES

    return False


def default_context():
    with open('./faq.txt', 'r', encoding='utf-8') as f:
        sys_prompt = f.read()

    return sys_prompt


def display_message_history():

    history = load_message_history()

    if history:
        for message in history:
            if message['role'] == 'user':
                st.chat_message("human").markdown(message['content'])
            elif message['role'] == 'assistant':
                st.chat_message("assistant").markdown(message['content'])


def select_prompt(ip: str):
    ss.ip = ip


def fetch_signedURLs_from_ids(ids: list):
    with open('./urls.json', 'r') as f:
        urls = json.load(f)

    signedURLs = []
    for ID in ids:
        signedURLs.append(urls[ID])

    return signedURLs
