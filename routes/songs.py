from flask import Blueprint, jsonify, request
from utils.data_manager import get_normalized_data, set_normalized_data

songs = Blueprint("songs", __name__)


@songs.route("/all", methods=["GET"])
def get_all_songs():
    """
    Fetches all song data in a normalized fashion and returns it
    to the user as a list of dictionaries

    Returns:
        dict: Dictionary containing song data as a list of records
        str: Message containing either a "Success" message or error message
        int: HTTP status code (200 for success, 500 for internal server error)
    """

    try:
        data_df = get_normalized_data()

        # Converting the DataFrame to 2D array with its headers
        songs_data = [data_df.keys().tolist(), *data_df.values.tolist()]

        # Converting the result to JSON and returning it
        return (
            jsonify(
                {
                    "data": songs_data,
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
        str: Message containing either a "Success" message or error message
        int: HTTP status code (200 for success, 404 for not found, 500 for internal server error).
    """
    try:
        data_df = get_normalized_data()

        # Keeping a record of the original headers
        original_headers = data_df.keys().tolist()

        # Setting 'title' as index for faster data retrieval
        data_df = data_df.set_index("title")

        # Finding song in dataframe, otherwise returning None
        song = data_df.loc[title] if title in data_df.index else None

        # If song has been found
        if song is not None:
            # Converting the Series to 2D and including headers
            song = [original_headers, song.values.tolist()]

            # Converting the data types of the values to their original data
            # types from Numpy data types
            song[1] = [cell.item() if "item" in dir(cell) else cell for cell in song[1]]

            # Inserting title at correct place in the values list
            index_of_title = original_headers.index("title")
            song[1].insert(index_of_title, title)

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


@songs.route("/title/<id>/rate", methods=["PATCH"])
def rate_song_by_id(id):
    """
    Updates a song's rating by id in the normalized data

    Args:
        id (str): The ID of the song to rate

    Returns:
        str: Message containing either a "Success" message or error message
        int: HTTP status code (200 for success, 404 for not found, 500 for internal server error)
    """
    try:
        json_data = request.get_json()
        new_rating = json_data["new_rating"]

        data_df = get_normalized_data()

        # Inserting a 'rating' column if not already present
        if "rating" not in data_df.columns:
            data_df = data_df.assign(rating=None)

        # Setting 'id' as index for faster data retrieval
        data_df = data_df.set_index("id")

        if id in data_df.index:
            # Updating the song rating
            data_df.at[id, "rating"] = new_rating

            # Resetting the index
            data_df = data_df.reset_index()

            # Converting the updated dataframe to dictionary
            new_songs_data = data_df.to_json()

            # Saving it in playlist.json
            set_normalized_data(new_songs_data)

            return (
                jsonify({"message": "Success", "status_code": 200}),
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
                    "message": "Error occurred while updating data",
                    "error": str(e),
                    "status_code": 500,
                }
            ),
            500,
        )
