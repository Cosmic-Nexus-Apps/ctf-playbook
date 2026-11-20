#!/usr/bin/env python3
"""Enumerate page.php?id=N and decode base64/plain comments, printing non-decoy messages.

Usage:
  python scan_page_ids.py http://TARGET:8081/page.php?id= 1 10000 [decoy-substring]

Default decoy substring: "not your lucky page"
"""
import sys
import base64
import re
from concurrent.futures import ThreadPoolExecutor
import requests

base = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
decoy = sys.argv[4] if len(sys.argv) > 4 else "not your lucky page"


def decode(text):
    try:
        return base64.b64decode(text + "=" * (-len(text) % 4)).decode("utf-8", "ignore")
    except Exception:
        return ""


def check(i):
    try:
        r = requests.get(base + str(i), timeout=6)
        if r.status_code != 200:
            return None
        found = []
        comments = re.findall(r"<!--(.*?)-->", r.text, re.S)
        for c in comments:
            s = c.strip()
            if not s:
                continue
            if re.fullmatch(r"[A-Za-z0-9+/=]{12,}", s):
                s = decode(s)
            if s and decoy not in s:
                found.append(s[:300])
        for b in re.findall(r"base64,([A-Za-z0-9+/=]{12,})", r.text):
            d = decode(b)
            if d and decoy not in d:
                found.append(d[:300])
        if found:
            return (i, found)
    except Exception:
        pass
    return None


with ThreadPoolExecutor(max_workers=20) as ex:
    for res in ex.map(check, range(start, end + 1)):
        if res:
            print("HIT", res, flush=True)
print("done")
