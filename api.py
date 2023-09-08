from flask import Flask, jsonify
from flask_cors import CORS
from routes.songs import songs

# Flask api setup
api = Flask(__name__)


api.register_blueprint(songs, url_prefix="/api/songs")
CORS(api)


@api.errorhandler(404)
def page_not_found(error):
    return (
        jsonify(
            {
                "message": "Route not found",
                "error": str(error),
                "status_code": 404,
            }
        ),
        404,
    )


if __name__ == "__main__":
    api.run(debug=True)
