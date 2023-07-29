import hashlib
import json
import os
import random

import requests
import urllib3

from ...typing import Dict, get_type_hints, sha256

url = "https://deepai.org"
model = ["gpt-3.5-turbo"]
supports_stream = True
needs_auth = False


def _create_completion(
    model: str, messages: list, stream: bool, session: requests.Session(), **kwargs
):
    def md5(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()[::-1]

    def get_api_key(user_agent: str) -> str:
        part1 = str(random.randint(0, 10**11))
        part2 = md5(user_agent + md5(user_agent + md5(user_agent + part1 + "x")))

        return f"tryit-{part1}-{part2}"

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    headers = {"api-key": get_api_key(user_agent), "user-agent": user_agent}

    files = {"chat_style": (None, "chat"), "chatHistory": (None, json.dumps(messages))}
    s = session
    print("Creating response")
    # try:
    #     r = session.post("https://api.deepai.org/chat_response", headers=headers, files=files, stream=True, timeout=100)
    # except requests.exceptions.ProxyError:
    #     print('Proxy error, retrying')
    #     proxies.remove(proxy)
    #     _create_completion(model=model, messages=messages, stream=stream, proxies=proxies, **kwargs)
    r = s.post(
        "https://api.deepai.org/chat_response",
        headers=headers,
        files=files,
        stream=True,
        timeout=100,
    )

    return r.text
