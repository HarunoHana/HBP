from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'

def project1_title():
    return 'This is JT Cho project 1page '