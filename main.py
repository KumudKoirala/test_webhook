from flask import Flask,request
import os 
import hmac
import hashlib
import json
import sys
set_token=os.environ.get("TOKEN")
set_app_secret=os.environ.get("APP_SECRET")
message_to_print=os.environ.get("USER")
received_updates = [] 

def is_x_hub_valid():
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return False
    signature=signature[len("sha256="):]
    computed_signature = hmac.new(
        set_app_secret.encode(),
        request.data,  # Use the raw payload (body) as the data to hash
        hashlib.sha256
    ).hexdigest()
    print(f"the signature is {signature}")
    sys.stdout.flush()
    return hmac.compare_digest(computed_signature, signature)
    
app=Flask(__name__)

@app.route('/')
def show_updates():
    return f'<pre>{json.dumps(received_updates, indent=2)}</pre>'

@app.route('/webhook',methods=["GET"])
def verify_webhook():
    set_token=os.environ.get("TOKEN")
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == set_token:
        print('Webhook verifed')
        sys.stdout.flush()
        return request.args.get('hub.challenge')
    else:
        print('Webhook Not verifed')
        sys.stdout.flush()
        return 'Bad Request',400
       
@app.route('/webhook',methods=["POST"])
def handle_webhook():
    print('Facebook request body:', request.json)
    if not is_x_hub_valid():
        print('Warning - request header X-Hub-Signature not present or invalid')
        sys.stdout.flush()
        return 'Unauthorized', 401
    print('X-Hub-Signature validated')
    
    if not request.json.get('entry') or not isinstance(request.json['entry'], list):
        print('Invalid update format')
        sys.stdout.flush()
        return 'Bad Request', 400
    received_updates.insert(0, request.json)
    print('Update received and saved')
    sys.stdout.flush()
    return 'OK', 200 

if __name__=='__main__':
    app.run(debug=True)