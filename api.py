from flask import Flask
from flask_cors import CORS
from routes.songs import songs

# Flask api setup
api = Flask(__name__)


api.register_blueprint(songs, url_prefix="/api/songs")
CORS(api)


if __name__ == "__main__":
    api.run(debug=True)
