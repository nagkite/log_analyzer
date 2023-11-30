import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Retrieve the PORT environment variable (default to 8080 if not set)
    port = int(os.environ.get('PORT', 8080))
    # Run the Flask app on all available IP addresses and the PORT environment variable
    app.run(host='0.0.0.0', port=port)
