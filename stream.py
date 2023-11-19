from flask import Flask, render_template, Response
from featureflags.client import CfClient, Target
import os
import time

app = Flask(__name__)
api_key = os.getenv('FF_API_KEY')
client = CfClient(api_key)

def stream():
    target = Target(identifier='alex', name="alex")
    old_message = ""
    while True:
        message = client.string_variation("message", target, "hello, world")
        if message != old_message:
            yield f"data: {message}\n\n"
            old_message = message
        time.sleep(5)  

@app.route('/message-stream')
def message_stream():
    # creates an HTTP response from the stream function's output. 
    # text/event-stream is set to indicate that this response is an SSE stream, tells the client (browser) to keep the connection open and listen for data sent from the server.
    return Response(stream(), mimetype='text/event-stream')

@app.route('/')
def hello_world():
    target = Target(identifier='alex', name="alex")
    message = client.string_variation("message", target, "hello, world")
    return render_template('stream.html', message=message)

# The threaded=True argument in app.run() allows Flask to handle each request in a separate thread, which is necessary for SSE to work correctly.
if __name__ == '__main__':
    app.run(threaded=True)
