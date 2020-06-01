# Standard library imports
import os
import glob

# Third Party imports
import psycopg2
import pandas as pd
import json

# Local application imports
from sql_queries import *

# DB_CREDENTIALS = "host=127.0.0.1 dbname=sparkifydb user=student password=student"
DB_CREDENTIALS = "host=127.0.0.1 dbname=sparkifydb user=postgres"
SONG_DATA_PATH = "data/song_data"
LOG_DATA_PATH = "data/log_data"
SONG_TABLE_COLS = ["song_id", "title", "artist_id", "year", "duration"]
ARTIST_TABLE_COLS = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]
TIME_TABLE_COLS = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]


def get_files(filepath):
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    return all_files


def import_data(filepath):
    """ Currently only gets first line """
    f = open(filepath, "r")
    return f.readline()


def validate_data(json_data):
    data_dict = json.loads(json_data)
    return data_dict


def create_dataframe(data_dict):
    df = pd.DataFrame([data_dict])
    return df.head(1)


def extract_data_from_df(df, cols):
    """ Currently only gets first row """
    df = df[cols]
    return df.values[0].tolist()


def connect_to_db():
    conn = psycopg2.connect(DB_CREDENTIALS)
    cur = conn.cursor()
    return cur, conn


def insert_data_to_table(cur, conn, df, insert_query):
    cur.execute(insert_query, df)
    conn.commit()


def import_data_from_directory(dir_path):
    """ Currently only gets first file """
    files = get_files(dir_path)
    json_data = import_data(files[0])
    validated_data = validate_data(json_data)
    return create_dataframe(validated_data)


def load_data_to_table(data_frame, insert_query, cols):
    relevant_data = extract_data_from_df(data_frame, cols)
    cur, conn = connect_to_db()
    insert_data_to_table(cur, conn, relevant_data, insert_query)


def main():
    song_data = import_data_from_directory(SONG_DATA_PATH)
    load_data_to_table(song_data, song_table_insert, SONG_TABLE_COLS)
    load_data_to_table(song_data, artist_table_insert, ARTIST_TABLE_COLS)

    log_data = import_data_from_directory(LOG_DATA_PATH)
    return True


if __name__ == "__main__":
    main()