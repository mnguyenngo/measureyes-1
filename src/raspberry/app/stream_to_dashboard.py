import plac
import time
import datetime
from utils.datastreamer import DataStreamer
from utils.datareader import DataReader


def convert_ts_timeofday(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')


@plac.annotations(
    face_data=("Path to face data.", "positional"),
    person_data=("Path to person data.", "positional"),
    api_url=("Dashboard URL", "option", "a", str))
def main(face_data, person_data, api_url=None):
    if api_url is None:
        api_url = "https://hidden-lowlands-41791.herokuapp.com/responses/1"

    last_run = int(datetime.date.today().strftime("%s"))  # midnight today
    print(last_run)

    dashboard = DataStreamer(
        api_url=api_url,
        face_data=face_data,
        person_data=person_data)

    while True:
        results = DataReader(face_data=face_data, person_data=person_data)
        htr_data = results.get_htr_data(time_format="unix")

        # subset only data after last_run time
        # last_run_in_unix = datetime.datetime.utcfromtimestamp(
        # last_run).strftime('%H:%M:%S')

        new_data = htr_data[htr_data['ts'] > last_run]
        print(new_data.shape)
        if new_data.shape[0] > 0:  # if there is any new data
            new_data['ts'] = new_data['ts'].apply(convert_ts_timeofday)
            data = {'processed_data': new_data.to_dict(orient="records")}
            response = dashboard.post(data)
            if response is True:
                last_run = int(time.time())  # update last_run
        time.sleep(30)


if __name__ == '__main__':
    plac.call(main)
