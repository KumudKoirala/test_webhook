from flask import Flask
import os 
TOKEN=os.environ.get("TOKEN")
APP_SECRET=os.environ.get("APP_SECRET")
message_to_print="HELLO"
app=Flask(__name__)

@app.route('/')
def home():
    return(message_to_print)

if __name__=='__main__':
    app.run()