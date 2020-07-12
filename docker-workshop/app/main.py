from flask import request
from flask_api import FlaskAPI, status
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app)

@app.route("/")
def index():
    return "Hello Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
