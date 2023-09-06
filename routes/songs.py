from flask import Blueprint, jsonify
from utils.data_manager import get_normalized_data

songs = Blueprint("songs", __name__)


@songs.route("/all", methods=["GET"])
def get_all_songs():
    """
    Fetches all song data in a normalized fashion and returns it
    to the user as a list of dictionaries

    Returns:
        dict: Dictionary containing song data as a list of records
        int: HTTP status code (200 for success, 500 for internal server error)
    """

    try:
        data_df = get_normalized_data()

        # Converting the DataFrame to JSON and returning it
        return (
            jsonify(
                {
                    "data": data_df.to_dict(orient="records"),
                    "message": "Success",
                    "status_code": 200,
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Error occurred while fetching data",
                    "error": str(e),
                    "status_code": 500,
                }
            ),
            500,
        )


@songs.route("/title/<title>", methods=["GET"])
def get_song_by_title(title):
    """
    Fetches a song's data by title from the normalized data and
    returns it to the user

    Args:
        title (str): The title of the song to fetch

    Returns:
        dict: A dictionary containing the song's data.
        int: HTTP status code (200 for success, 404 for not found, 500 for internal server error).
    """
    try:
        data_df = get_normalized_data()

        # Setting 'title' as index for faster data retrieval
        data_df = data_df.set_index("title")

        # Finding song in dataframe, otherwise returning None
        song = data_df.loc[title] if title in data_df.index else None

        # If song has been found
        if song is not None:
            # Including title in final result
            song = {**song.to_dict(), "title": title}

            return (
                jsonify({"data": song, "message": "Success", "status_code": 200}),
                200,
            )

        else:
            return (
                jsonify(
                    {
                        "message": "Song not found",
                        "error": "Song not found in the data",
                        "status_code": 404,
                    }
                ),
                404,
            )

    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Error occurred while fetching data",
                    "error": str(e),
                    "status_code": 500,
                }
            ),
            500,
        )
