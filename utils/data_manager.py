import os, json
import pandas as pd
import numpy as np

# Creating path to playlist.json
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "data", "playlist.json")


def get_normalized_data():
    """
    Loads data from playlist.json in a normalized fashion and returns it
    as a dataframe object

    Returns:
        pandas.DataFrame: The dataframe containing the normalized data
        from playlist.json
    """

    # Loading the JSON data from the file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Extracting columns from the data
    columns = data.keys()

    # Creating a dataframe with the columns extracted earlier and the data
    # from the playlist JSON file
    df = pd.DataFrame(data, columns=columns)
    df = df.replace({np.nan: None})

    return df


def set_normalized_data(data):
    """
    Sets the normalized back data to playlist.json

    Arguments:
        data (dict): The dataframe that will saved in playlist.json
    """
    # Loading the JSON data from the file
    with open(file_path, "w") as file:
        file.write(data)
