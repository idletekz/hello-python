from flask import Flask, render_template, jsonify
from featureflags.client import CfClient, Target
import os

app = Flask(__name__)

client = None
api_key = os.getenv('FF_API_KEY')
client = CfClient(api_key)

@app.route('/')
def hello_world():
    target = Target(identifier='alex', name="alex")
    message = client.string_variation("message", target, "hello, world")
    return render_template('hello.html', message=message)

@app.route('/get-message')
def get_message():
    target = Target(identifier='alex', name="alex")
    message = client.string_variation("message", target, "hello, world")
    return jsonify(message=message)

def handle_app():
    app.run(debug=True)

if __name__ == '__main__':
    handle_app()
    client.close();
