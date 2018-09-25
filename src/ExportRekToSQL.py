"""
Export AWS Rekognition response jsons contained in a specified path/dir to Postgres database.

To run from terminal shell:    $ python PipeRekToSQL.py --path <"path/data_dir/">

For help from terminal shell:  $ python PipeRekToSQL.py --help

Constituent Functions:
-- queue_jsons(path)
-- rekognition_json_to_df(path, filter_poseNAs=False)
-- face_detected_bool(d)
-- insert_rekdf_to_SQL(connection, df)
"""


import json
import numpy as np
import pandas as pd
import os
import shutil
import argparse

from pandas.io.json import json_normalize
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, Integer, Float



connection_str = 'postgresql:///measureyes'
engine = create_engine(connection_str, echo=False)


def queue_jsons(path):
    """
    From response directory, return a list of path/file(s) to be fed into rekognition_json_to_df.
    path -- (str) may be absolute or relative from measureyes/src/
        example: "../data/<subdir>/".
    """
    f_list = os.listdir(path)

    queue = [path + file for file in f_list]
    queue.sort()
    return queue


def rekognition_json_to_df(path, filter_poseNAs=False):
    """Convert AWS Rekognition output json into Pandas DataFrame.
    Works for json responses written by AWS Rekognition GetFaceSearch function (or as run in VidFaceSearch.py)

    Arguments:
        path -- (string) path/file
        filter_poseNAs -- (bool) If True, includes only data in which a face pose was detected. If False,
                           return records for all unique persons detected and indexed in video.
    """

    with open(path) as f:
        d = json.load(f)

    df = json_normalize(d['Persons'], meta='Face', record_prefix=True)

    if not face_detected_bool(d):
        # If no faces were detected, create blank (NaN) columns for missing keys in json source file.
        df['Person.Face.BoundingBox.Top'] = np.NaN
        df['Person.Face.BoundingBox.Left'] = np.NaN
        df['Person.Face.Pose.Pitch'] = np.NaN
        df['Person.Face.Pose.Yaw'] = np.NaN

    cols_raw = [
            "Timestamp",
            "Person.Index",
            "Person.Face.BoundingBox.Top", # BoundingBox Top and Left for position of the face in the frame
            "Person.Face.BoundingBox.Left",
            "Person.Face.Pose.Pitch",
            "Person.Face.Pose.Yaw",
        ]

    source = path.split("/")[-1]
    video = source.split("_response_")[0] + ".mp4"

    rows_filtered = df["Person.Face.Pose.Pitch"].map(lambda x: not np.isnan(x)) # filter out frames with no faces
    if filter_poseNAs:
        df = df.loc[rows_filtered, cols_raw]
    else:
        df = df[cols_raw]

    df["SourceFile"] = source
    df["Video"] = video

    # Reorder columns
    cols_reordered = [
            "Video",
            "SourceFile",
            "Timestamp",
            "Person.Index",
            "Person.Face.Pose.Yaw",
            "Person.Face.Pose.Pitch",
            "Person.Face.BoundingBox.Top",
            "Person.Face.BoundingBox.Left"
        ]

    df = df[cols_reordered]

    # Rename columns
    cols_renamed = [
            "video",
            "source_file",
            "timestamp",
            "person_index",
            "face_yaw",
            "face_pitch",
            "face_box_top", # face bounding box location
            "face_box_left"
        ]
    df.columns = cols_renamed

    # Order and index records by Timestamp
    df.sort_values("timestamp", inplace=True)
    df.index = np.arange(len(df))

    return df


def face_detected_bool(d):
    """
    Support function for rekognition_json_to_df()
    Return boolean test of whether one or more Face detections were recorded
    in an AWS Rekognition response.
    d -- python dictionary resulting from json.load(json_source_file)"""
    bool = set()
    for idx in range(len(d['Persons'])):
        person = d['Persons'][idx]['Person'].keys()
        bool.add('Face' in person)
    return True in bool



def insert_rekdf_to_SQL(connection, df):
    """Append parsed AWS Rekogntion response df to the rekmaster table in Postgres.
    """
    dtypes = {
        "video": VARCHAR(),
        "source_file": VARCHAR(),
        "timestamp": Integer(),
        "person_index": Integer(),
        "face_yaw": Float(32),
        "face_pitch": Float(32),
        "face_box_top": Float(32),
        "face_box_left": Float(32)
    }

    df.to_sql('rekmaster', con=connection, if_exists='append', index=False, dtype=dtypes)


if __name__ == "__main__":


    # Establish connection to Postgres DB
    connection_str = 'postgresql:///measureyes'
    engine = create_engine(connection_str, echo=False)

    # Configure to receive path/data_dir from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help=('''(string) path/data_dir/ containing json files to be
    parsed and inserted into SQL; example -- path relative to measureyes/src/: "../data/Vid_response/"'''))
    args = parser.parse_args()

    # For ea file, parse and insert into SQL
    for path_file in queue_jsons(args.path):
        df = rekognition_json_to_df(path_file)
        insert_rekdf_to_SQL(engine, df)
        print("Inserted into SQL: {}".format((path_file).split('/')[-1]))

    print("\nJOB COMPLETE")
