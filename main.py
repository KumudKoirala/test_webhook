from flask import Flask,request
import os 
import hmac
import hashlib
import json
set_token=os.environ.get("TOKEN")
set_app_secret=os.environ.get("APP_SECRET")
message_to_print=os.environ.get("USER")
received_updates = [] 

def is_x_hub_valid():
    signature = request.headers.get('X-Hub-Signature')
    if not signature:
        return False
    hash = hmac.new(APP_SECRET.encode(), json.dumps(request.get_json()).encode(), hashlib.sha1)
    calculated_signature = f"sha1={hash.hexdigest()}"
    
    return signature == calculated_signature ## compare and return the boolean
    
app=Flask(__name__)

@app.route('/')
def show_updates():
    return f'<pre>{json.dumps(received_updates, indent=2)}</pre>'

@app.route('/webhook',methods=["GET"])
def verify_webhook():
    set_token=os.environ.get("TOKEN")
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == set_token:
       return request.args.get('hub.challenge')
    else:
        return 'Bad Request',400
       
@app.route('/webhook',methods=["POST"])
def handle_webhook():
    print('Facebook request body:', request.json)
    if not is_x_hub_valid():
        print('Warning - request header X-Hub-Signature not present or invalid')
        return 'Unauthorized', 401
    print('X-Hub-Signature validated')
    
    if not request.json.get('entry') or not isinstance(request.json['entry'], list):
        print('Invalid update format')
        return 'Bad Request', 400
    received_updates.insert(0, request.json)
    print('Update received and saved')
    return 'OK', 200 

if __name__=='__main__':
    app.run()