"""
Detect and aggregate statistics on Head Turns (HTs)
"""

import numpy as np
import pandas as pd

from sqlalchemy import create_engine



class HTDetect(object):
    """
    Identify and tabulate distinct head-turns (HTs) from raw computer-vision data
    based on specified pose, dwell and 'break' thresholds. Aggregate statistics
    on HT responses including HT counts and head-turn rate (HTR).

    INITIALIZATION PARAMS
        source: (string) Unique ID name for Postgres table containing target data

    METHODS
        main(yaw_threshold=45, pitch_threshold=45, dwell_threshold=1.5, HT_break=1.5)

    ATTRIBUTES
        all_records_df: (DataFrame) raw data from source
        ttl_persons: (int) number of distinct persons detected in video
        facing_camera_df: (DataFrame) all rows from source recording a face turned
                           at any angle toward the camera
        filtered_by_pose: (DataFrame) facing_camera_df records filtered by face pose
                          thresholds
        HTs_df: (DataFrame) chronologically sorted HTs with timestamp, dwell and person_id
        HTers: (int) number of distinct persons making HTs detected in video
        HTR: (float) ratio of HTers to ttl_persons

    """
    def __init__(self, source):
        self.source = source
        self.all_records_df = None
        self.ttl_persons = None
        self.facing_camera_df = None
        self.filtered_by_pose = None
        self.HTs_df = None
        self.HTers = None
        self.HTR = None


        self._connection_str = 'postgresql:///measureyes'
        self._conn = None


    def main(self, yaw_threshold=45, pitch_threshold=45, dwell_threshold=1.5,
             HT_break=1.5, print=False):
        """Identify and tabulate distinct head-turns (HTs) from raw computer-vision data
        based on specified pose, dwell and 'break' thresholds.

        ARGS
            yaw_threshold=45: (int) head pose degrees left and right plus or minus zero (facing camera)
                              within which to qualify an HT
            pitch_threshold=45: (int) head pose degrees up and down plus or minus zero (facing camera)
                                within which to qualify an HT
            dwell_threshold=1.5: (float) minimum seconds of dwell time (viewer facing camera)
                                 required to qualify an HT
            HT_break=1.5: (float) minimum seconds constituting a break between multiple
                          views or HTs performed by a single viewer; breaks below
                          `HT_break` are ignored when counting a single, continuous HT
            print=False: (bool) If True, print a summary of HT detection results.
        """
        # Disable Pandas SettingWithCopy error:
        # see https://stackoverflow.com/questions/42105859/pandas-map-to-a-new-column-settingwithcopywarning
        pd.options.mode.chained_assignment = None

        # Reset attribute HTs_df ea time main() is run. Facilitates tuning HT parameters.
        self.HTs_df = pd.DataFrame({'HT_start': [],
                                    'HT_dwell': [],
                                    'person_index': []
                                    })
        self._get_all_records()
        self._pose_filter(yaw_threshold, pitch_threshold)
        self._build_HT_df(dwell_threshold, HT_break)

        if print:
            self._print_results(yaw_threshold, pitch_threshold, dwell_threshold,
            HT_break)


    def _print_results(self, yaw_threshold=45, pitch_threshold=45, dwell_threshold=1.5,
             HT_break=1.5):
         print("""
 Source ID: {}
 Total Persons Detected: {}
 Total HTs Detected: {}
 Total Distinct HTers: {}
 Head-Turn Rate: {:.3f}
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Head xTurn Parameters:
     Yaw Threshold (max allowable face angle left or right of camera): {} degrees
     Pitch Threshold (max allowable angle up or down from camera): {} degrees
     Minimum dwell to qualify: {} seconds
     Minimum duration (break) between multiple HTs by single person: {} seconds
 """.format(self.source,
            self.ttl_persons,
            len(self.HTs_df),
            self.HTers,
            self.HTers / self.ttl_persons,
            yaw_threshold,
            pitch_threshold,
            dwell_threshold,
            HT_break
            )
        )


    def _get_all_records(self):
        """Query DB for all records in which a person was detected; return as dataframe."""
        self._conn = create_engine(self._connection_str, echo=False)

        QUERY = ("""SELECT *
                    FROM {}
                    ORDER BY person_index, timestamp;
                    """.format(self.source)
                    )

        self.all_records_df = pd.read_sql_query(QUERY, self._conn)
        self.ttl_persons = len(self.all_records_df['person_index'].unique())


    def _pose_filter(self, yaw_threshold=45, pitch_threshold=45):

        cols_1 = ['timestamp', 'person_index', 'face_yaw', 'face_pitch']

        # Drop all records where no face was detected
        self.facing_camera_df = self.all_records_df.dropna(subset=['face_yaw'])
        self.facing_camera_df = self.facing_camera_df[cols_1]

        # Filter remaining records by yaw and pitch thresholds
        self.filtered_by_pose = self.facing_camera_df.loc[
            (self.facing_camera_df['face_yaw'].abs() <= yaw_threshold) & \
            (self.facing_camera_df['face_pitch'].abs() <= pitch_threshold)
        ]


    def _build_HT_df(self, dwell_threshold, HT_break):
        """Combine HT tables for individuals to form HTs_df. Compute count of
        viewers (HTers) and HTR.
        """
        faces = self.filtered_by_pose['person_index'].unique()

        # Cycle through all potential viewers and append to HTs_df
        for ID in faces:
            next_ID = self._HTs_by_person(ID, dwell_threshold, HT_break)
            self.HTs_df = self.HTs_df.append(next_ID, ignore_index=True)

        self.HTs_df.sort_values('HT_start', inplace=True)
        self.HTs_df.index = range(1, len(self.HTs_df) + 1)
        self.HTs_df['person_index'] = self.HTs_df['person_index'].astype('int')
        self.HTs_df['HT_start'] = self.HTs_df['HT_start'].astype('int')

        # Compute count of persons making HTs and HTR
        self.HTers = len(self.HTs_df['person_index'].unique())
        self.HTR = self.HTers / self.ttl_persons


    def _HTs_by_person(self, ID, dwell_threshold, HT_break):
        """Construct dataframe of HTs recorded for a single person_id
        """
        # Grab rows for a single person_index and re-index this subset
        df_indiv = self.filtered_by_pose[self.filtered_by_pose['person_index'] == ID]
        df_indiv.index = range(len(df_indiv))

        # Add column for time deltas from one row to the next
        df_indiv['timediff'] = df_indiv['timestamp'].diff().fillna(0)

        # Grab indeces where time deltas indicate the starting times of distinct HTs
        foo = list(df_indiv[df_indiv['timediff'] == 0].index) # grabs first (or only) HT start
        bar = list(df_indiv[df_indiv['timediff'] >= HT_break * 1000].index)
        foo.extend(bar)
        HT_starts = np.array(foo)

        # Grab indeces at ends of distinct HTs
        if len(HT_starts) == 1: # If only one HT...
            HT_ends = [-1]
        else:
            HT_ends = list(HT_starts[1:] - 1)
            HT_ends.append(-1)
        HT_ends = np.array(HT_ends)

        # Generate array of HT dwell times
        dwells = []
        if len(HT_starts) == 1:
            dwells.append(df_indiv.iloc[-1, 0] - df_indiv.loc[0, 'timestamp'])
        else:
            for start, end in zip(HT_starts, HT_ends):
                start_time = df_indiv.iloc[start, 0]
                end_time = df_indiv.iloc[end, 0]
                dwells.append(end_time - start_time)
        dwells = np.array(dwells)

        # Construct HT table for single person_index
        df_HTs = df_indiv.iloc[HT_starts, :]
        df_HTs['dwell'] = dwells / 1000.

        cols_2 = ['timestamp', 'dwell', 'person_index']

        df_HTs = df_HTs[cols_2]

        cols_renamed = ['HT_start', 'HT_dwell', 'person_index']
        df_HTs.columns = cols_renamed

        # Filter individual HT table by dwell threshold
        return df_HTs[df_HTs['HT_dwell'] >= dwell_threshold]



if __name__ == "__main__":

    target = 'Measureyes_0924_01'
    test = HTDetect(target)
    test.main(print=True)
    print('')
    print(test.HTs_df.head(10))
