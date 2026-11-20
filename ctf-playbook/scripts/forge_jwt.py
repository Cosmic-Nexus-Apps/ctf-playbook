#!/usr/bin/env python3
"""Forge an HS256 JWT.

Usage:
  python forge_jwt.py <secret> <iss> <sub> <scope>

Example:
  python forge_jwt.py 'S3cr3t' house-atriedes ducal-scribe decree:draft
"""
import sys
import hmac
import json
import base64
import hashlib


def b64u(data):
    if isinstance(data, str):
        data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


secret, iss, sub, scope = sys.argv[1:5]
header = {"alg": "HS256", "typ": "JWT"}
payload = {"iss": iss, "sub": sub, "scope": scope}
signing_input = b64u(json.dumps(header, separators=(",", ":"))) + "." + \
    b64u(json.dumps(payload, separators=(",", ":")))
sig = b64u(hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest())
print(signing_input + "." + sig)
