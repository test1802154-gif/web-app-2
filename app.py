from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    api_key = os.environ.get('API_KEY', 'No Key Found')
    return f"🚀 App-1 is Running! Secret API Key used: {api_key}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
