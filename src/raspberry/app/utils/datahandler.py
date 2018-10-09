"""Class object that handles recording of data either to csv or SQL.
"""
import time


class DataHandler():
    def __init__(self, measure, path, method='csv'):
        """Records the results from the object detection video feed.

        Arguments:
            measure (str): 'faces' or 'persons'
            path (str): path to directory for data
            method (str): 'csv' or 'sql'

        Note: sql method is not supported yet
        """
        assert measure in ['faces', 'persons']
        assert method in ['csv', 'sql']
        self.method = method
        self.start_time = int(time.time())
        self.csvfilename = f'{path}/{measure}_{self.start_time}.csv'
        self.csvfile = None

    def makefile(self):
        """Creates a csv file to record the results"""
        self.csvfile = open(self.csvfilename, 'a')
        header = "ts,label,id,confidence,startX,startY,endX,endY\n"
        self.csvfile.write(header)
        self.csvfile.write("{},{},0,0,0,0,0,0\n".format(
            self.start_time, 'videostart'))

        print("Object detection results are being recorded")
        print("""Run the following command in a new terminal to stream the
              output data to the dashboard:""")
        print(f'''python stream_to_dashboard.py \
../data/output/faces_{self.start_time}.csv \
../data/output/persons_{self.start_time}.csv -a \
"https://hidden-lowlands-41791.herokuapp.com/responses/1"''')

    def write(self, data):
        """Writes each detection event into the csv file"""
        self.csvfile.write(f"{data}\n")
        self.csvfile.flush()

    def close(self):
        """Adds the last line of data to indicate videoend and closes the file
        """
        end_time = int(time.time())
        self.csvfile.write("{},{},0,0,0,0,0,0\n".format(
            end_time, 'videoend'))
        self.csvfile.close()
