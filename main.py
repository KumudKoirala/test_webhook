from flask import Flask

message_to_print="Hello"
app=Flask(__name__)

@app.route('/')
def home():
    return(message_to_print)

if __name__=='__main__':
    app.run()