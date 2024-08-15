#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 02:33:04 2024

@author: dev
"""

from huggingface_hub import InferenceClient
import os


try:
    HF_API_TOKEN = os.environ['HF_API_TOKEN']
except:
    with open('./(huggingface)token', 'r') as f:
        HF_API_TOKEN = f.read()

os.environ['HF_API_TOKEN'] = HF_API_TOKEN


def hf_ask(prompt: str = "Introduce yourself",
           system_prompt: str = "None",
           log: bool = False):

    client = InferenceClient(
        "meta-llama/Meta-Llama-3-8B-Instruct",
        token=HF_API_TOKEN,
    )

    MESSAGES = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    params = {
        "temperature": 0.0,
        "max_tokens": 500000,
        "stream": True
    }

    st_text = []
    for message in client.chat_completion(
            messages=MESSAGES,
            **params
    ):
        st_text.append(message.choices[0].delta.content)
        print(message.choices[0].delta.content, end="")

    st_text = "".join(st_text)

    MESSAGES.append({
        "role": "assistant",
        "content": st_text
    })

    return st_text
