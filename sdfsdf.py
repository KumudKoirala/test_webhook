import hmac
import hashlib
import json
from flask import Flask,request

hash = hmac.new("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".encode(), json.dumps(request.get_json()).encode(), hashlib.sha1)