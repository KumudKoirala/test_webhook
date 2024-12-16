from flask import Flask,request
import os 
set_token=os.environ.get("TOKEN")
set_app_secret=os.environ.get("APP_SECRET")
message_to_print=os.environ.get("USER")
app=Flask(__name__)

@app.route('/')
def home():
    return('welcome_home')

@app.route('/webhook',methods=["GET","POST"])
def index():
    if 'hub.mode' in request.args:
        mode=request.args.get('hub.mode')
    if 'hub.verify_token' in request.args:
        token=request.args.get('hub.verify_token')
    if 'hub.challenge' in request.args:
        challenge=request.args.get('hub.challenge')
    if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
        mode=request.args.get('hub.mode')
        token=request.args.get('hub.verify_token')
        if mode=='subscribe' and token==set_token:
            print('WEBHOOK VERIFIED')
            challenge=request.args.get('hub.challenge')
            return(challenge,200)
        else:
            return ("Invalid mode or token or both",403)
    else:
        return("Error: Missing required parameters: mode and verify_token", 400 )


if __name__=='__main__':
    app.run()