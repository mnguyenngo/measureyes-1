"""
"""
import time


class DataHandler():
    def __init__(self, measure, path=None, method='csv'):
        """Records the results from the object detection video feed.

        Arguments:
            measure (str): 'faces' or 'persons'
            path (str): path to directory for data
            method (str): 'csv' or 'sql'

        Note: sql method is not supported yet
        """
        self.method = method
        self.start_time = int(time.time())
        self.csvfilename = f'{path}/{measure}_{self.start_time}.csv'
        assert method in ['csv', 'sql']
        if self.method == 'csv':
            self.csvfile = open(self.csvfilename, 'a')
            self.startup()

    def startup(self):
        header = "ts,label,id,confidence,startX,startY,endX,endY\n"
        self.csvfile.write(header)
        self.csvfile.write("{},{},0,0,0,0,0,0\n".format(
            self.start_time, 'videostart'))

    def write(self, data):
        self.csvfile.write(f"{data}\n")

    def close(self):
        end_time = int(time.time())
        self.csvfile.write("{},{},0,0,0,0,0,0\n".format(
            end_time, 'videoend'))
        self.csvfile.close()
