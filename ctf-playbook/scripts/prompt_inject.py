#!/usr/bin/env python3
"""Send a prompt to an LLM-agent endpoint and print the trace.

Usage:
  python prompt_inject.py http://TARGET:8090 <TOKEN> "<body>" ["subject"]

Retry 3-6 times: agent answers are probabilistic.
"""
import sys
import requests

url = sys.argv[1].rstrip("/")
token = sys.argv[2]
body = sys.argv[3]
subject = sys.argv[4] if len(sys.argv) > 4 else "safe conduct"
r = requests.post(url + "/petition", json={"subject": subject, "body": body},
                  headers={"Authorization": "Bearer " + token}, timeout=900)
print("status", r.status_code)
j = r.json()
for t in j.get("trace", []):
    text = str(t.get("text", ""))[:2000]
    print(t.get("kind"), ":", text)
text = str(j.get("reply", ""))[:2000]
print("REPLY:", text)
