from flask import Flask

# Flask api setup
api = Flask(__name__)

if __name__ == "__main__":
    api.run(debug=True)
