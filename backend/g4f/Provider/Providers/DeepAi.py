import json
import hashlib
import requests
import random
import math

from ...typing import sha256, Dict, get_type_hints

url = 'https://deepai.org'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False
working = True


def convert_code(t):
    p = [0] * 64
    for q in range(64):
        p[q] = int(4294967296 * math.sin((q + 1) % math.pi))

    w, y = 1732584193, 4023233417
    ea = [w, y, ~w, ~y]
    Z = [4]
    A = (t.encode('utf-8') + b'\x80').decode('latin-1')
    z = len(A)
    t = (z - 1) // 4 + 2 | 15
    Z[0] = 8 * z
    z -= 1
    while z >= 0:
        Z.append(ord(A[z]) << (8 * z))
        z -= 1

    q = 0
    while q < t:
        z = ea.copy()
        A = 0
        while A < 64:
            w = z[0] + ((w & y) | (~w & z[3]) | (w ^ y ^ z[3]) | (y ^ (w | ~z[3]))) + p[A] + (
                    Z[q | ([A, 5 * A + 1, 3 * A + 5, 7 * A][2] & 15)]
                    << ([7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21][14])
            ) | (
                    -([7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21][6])
                )

            A += 1
        A = 4
        while A:
            ea[A - 1] += z[A - 1]
            A -= 1
        q += 16

    t = ""
    A = 0
    while A < 32:
        t += hex((ea[A >> 3] >> (4 * (1 ^ A))) & 15)[2:]
        A += 1

    return t[::-1]


def _create_completion(model: str, messages: list, stream: bool, session: requests.Session(), **kwargs):
    def md5(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()[::-1]

    def get_api_key(user_agent: str) -> str:
        part1 = str(random.randint(0, 10 ** 11))
        part2 = md5(user_agent + md5(user_agent + md5(user_agent + part1 + "x")))

        return f"tryit-{part1}-{part2}"

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    h = str(round(1E11 * random.random()))
    header = "tryit-" + h + "-" + convert_code(
        user_agent + convert_code(user_agent + convert_code(user_agent + h + "x")))
    headers = {
        "Api-Key": header,
    }
    print(header)
    files = {
        "chat_style": ("chat_style", "chat"),
        "chatHistory": (None, json.dumps(messages)),
        "model": "genius"
    }

    session = session
    r = session.post("https://api.deepai.org/make_me_a_pizza", headers=headers, params=files)

    return r
