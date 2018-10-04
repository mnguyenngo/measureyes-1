"""Class object to read raw data output and provide methods to plot the data
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime


class DataReader():
    def __init__(self, face_data, person_data, read_from='csv'):
        """Process raw object detection data and provides different plot
        outputs

        Arguments:
            face_data (df)
            person_data (df)

        Attributes:

        """
        assert read_from in ['csv', 'dataframe', 'df']
        if read_from == 'csv':
            face_data = pd.read_csv(face_data)
            person_data = pd.read_csv(person_data)
        self.raw_face_data = face_data
        self.raw_person_data = person_data
        self.clean_face_data = self.process_data(face_data)
        self.clean_person_data = self.process_data(person_data)
        self.start_date = None
        self.end_date = None
        self.x_axis_ts = self.get_timeframe()
        self.x_axis_timeofday = self.ts_to_timeofday(self.x_axis_ts)
        self.htr_data = self.get_htr_data()

    def process_data(self, raw_df):
        """Returns a groupby object grouped by each second"""
        raw_gb = raw_df.groupby(by=['ts', 'id'])
        raw_gb_mean = raw_gb.mean().reset_index()

        # add object centroid to the df
        raw_gb_mean['X'] = raw_gb_mean.apply(
            lambda x: self.get_object_centroid(x, 'X'), axis=1)
        raw_gb_mean['Y'] = raw_gb_mean.apply(
            lambda x: self.get_object_centroid(x, 'Y'), axis=1)

        # add time of day column so that we don't need to read ts
        raw_gb_mean = self.add_timeofday_col(raw_gb_mean)
        return raw_gb_mean

    def get_object_centroid(self, row, axis='X'):
        """Iterates through each row to return the average of start and end
        Pandas apply function
        """
        if axis == 'X':
            return (row['startX'] + row['endX']) / 2
        elif axis == 'Y':
            return (row['startY'] + row['endY']) / 2
        else:
            print("'axis' must be 'X' or 'Y'")
            raise

    def add_timeofday_col(self, df):
        df['dt'] = pd.to_datetime(df['ts'])
        df['time_of_day'] = df['dt'].apply(lambda x: x.strftime('%H:%M:%S'))
        df = df.drop('dt', axis=1)
        return df

    def ts_to_timeofday(self, l_ts):
        timeofday = []
        for ts in l_ts:
            timeofday.append(
                datetime.utcfromtimestamp(ts).strftime('%H:%M:%S'))
        assert len(timeofday) == len(l_ts)
        return timeofday

    def get_timeframe(self):
        """Returns min and max ts from processed data"""
        min_ts_face = self.clean_face_data['ts'].min()
        min_ts_person = self.clean_person_data['ts'].min()
        max_ts_face = self.clean_face_data['ts'].max()
        max_ts_person = self.clean_person_data['ts'].min()
        return np.arange(min(min_ts_face, min_ts_person),
                         max(max_ts_face, max_ts_person), 1)

    def get_htr_data(self):
        count_faces = self.clean_face_data.groupby(by='ts').nunique()
        count_persons = self.clean_person_data.groupby(by='ts').nunique()

        infill_count_faces = [count_faces.loc[ts, 'id']
                              if ts in count_faces.index
                              else 0 for ts in self.x_axis_ts]
        infill_count_persons = [count_persons.loc[ts, 'id']
                                if ts in count_persons.index
                                else 0 for ts in self.x_axis_ts]

        htr_df = pd.DataFrame(data={
            'ts': self.x_axis_timeofday,
            'faces': infill_count_faces,
            'persons': infill_count_persons})

        return htr_df

    def save_htr_data(self, path=None, method='csv'):
        """Write processed data to csv or sql."""
        pass

    # plot methods
    def stackarea(self, figsize=(6, 6), timestep=1, bin_time_by="15Min"):
        """Returns a stacked area plot with persons on the bottom"""
        fig, ax = plt.subplots(figsize=figsize)

        if bin_time_by is None:
            X = self.x_axis_timeofday
            Y1 = self.htr_data['faces']
            Y2 = self.htr_data['persons'] - Y1
            title = "Pedestrians and Head-Turns Per Second"
        else:
            X, Y1, Y2, title = self.plot_attr_for_bin(bin_time_by)

        ax.stackplot(X, np.array([Y1, Y2]), labels=['head-turn'],
                     edgecolor='white')
        xticks = ax.get_xticks()
        ax.set_xticks(xticks[::timestep])
        plt.xlabel('time')
        plt.ylabel(f'persons per {bin_time_by}')
        plt.title(title)
        plt.legend()
        plt.show()

    def stackbar(self, figsize=(6, 6), timestep=1, bin_time_by="15Min",
                 width=0.005):
        """Returns a stacked bar plot with persons on the bottom"""
        fig, ax = plt.subplots(figsize=figsize)

        if bin_time_by is None:
            X = self.x_axis_timeofday
            Y1 = self.htr_data['faces']
            Y2 = self.htr_data['persons'] - Y1
            title = "Pedestrians and Head-Turns Per Second"
        else:
            X, Y1, Y2, title = self.plot_attr_for_bin(bin_time_by)

        ax.bar(X, Y1, color='#5392ff', width=width, label="head-turn")
        ax.bar(X, Y2, color='#ff5c49', width=width, bottom=Y1)
        xticks = ax.get_xticks()
        ax.set_xticks(xticks[::timestep])
        plt.xlabel('time')
        plt.ylabel(f'persons per {bin_time_by}')
        plt.title(title)
        plt.legend()
        plt.show()

    def plot_attr_for_bin(self, bin_time_by):
        htr = self.htr_data.copy()
        htr['dt'] = htr['ts'].apply(pd.to_datetime)
        htr_gb = htr.groupby(pd.Grouper(key='dt', freq=bin_time_by)).sum()
        X = htr_gb.index
        Y1 = htr_gb['faces']
        Y2 = htr_gb['persons'] - htr_gb['faces']
        title = f"Pedestrians and Head-Turns Per {bin_time_by.capitalize()}"
        return X, Y1, Y2, title

    def plotbar(self, metric='face', figsize=(6, 6), timestep=5):
        """

        Arguments:
            metric (str): 'face' or 'persons'
        """
        fig, ax = plt.subplots(figsize=figsize)
        X = self.x_axis_timeofday

        if metric == 'face':
            Y = self.htr_data['faces']
        elif metric == 'person':
            Y = self.htr_data['persons']
        else:
            print("'metric' must be 'face' or 'person'")
            raise
        ax.bar(X, Y, color='#5392ff')
        xticks = ax.get_xticks()
        ax.set_xticks(xticks[::timestep])
        plt.show()

    def plotline(self, metric='face', figsize=(6, 6), timestep=5):
        """

        Arguments:
            metric (str): 'face' or 'persons'
        """
        fig, ax = plt.subplots(figsize=figsize)
        X = self.x_axis_timeofday
        if metric == 'face':
            Y = self.htr_data['faces']
        elif metric == 'person':
            Y = self.htr_data['persons']
        else:
            print("'metric' must be 'face' or 'person'")
            raise
        ax.plot(X, Y, color='#5392ff')
        xticks = ax.get_xticks()
        ax.set_xticks(xticks[::timestep])
        plt.show()
