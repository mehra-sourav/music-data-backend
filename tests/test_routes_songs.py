import pytest, os, sys
from flask import Flask

api_file_loc = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(api_file_loc)

from routes.songs import songs


@pytest.fixture
def api():
    api = Flask(__name__)
    api.register_blueprint(songs)
    return api


def test_get_all_songs(api):
    client = api.test_client()

    response = client.get("/all")
    assert response.status_code == 200

    data = response.get_json()
    assert "data" in data
    assert "message" in data
    assert "status_code" in data


def test_get_song_by_title(api):
    client = api.test_client()

    # Testing with an existing title
    title = "3AM"
    response = client.get(f"/title/{title}")

    assert response.status_code == 200
    data = response.get_json()

    assert "data" in data
    assert "message" in data
    assert "status_code" in data

    # Testing with a non-existing title
    title = "NonExistentSong"
    response = client.get(f"/title/{title}")

    assert response.status_code == 404
    data = response.get_json()

    assert "message" in data
    assert "status_code" in data


if __name__ == "__main__":
    pytest.main()
