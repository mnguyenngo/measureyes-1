import requests
import time


class DataStreamer():
    def __init__(self, api_url=None, face_data=None, person_data=None):
        self.api_base_url = "https://hidden-lowlands-41791.herokuapp.com"
        self.api_endpoint = "responses/1"
        if api_url is None:
            self.api_url = f"{self.api_base_url}/{self.api_endpoint}"
        else:
            self.api_url = api_url
        self.start_time = int(time.time())
        self.log_file = f"../data/stream/{self.start_time}_api.log"

    def post(self, data):
        """Create temp json file and run shell script to post to a dashboard
        API

        Arguments:
            data (json/dict)

        Usage:
            Shell Script:
                $ http POST \
                https://hidden-lowlands-41791.herokuapp.com/responses/1 \
                @me_data.json
        """
        assert type(data) is dict
        try:
            resp = requests.post(self.api_url, json=data)
            current_time = int(time.time())
            with open(self.log_file, 'a') as f:
                f.write(f"Timestamp: {current_time}; {resp.status_code}\n")
                if resp.status_code == 201:
                    f.write(f"{len(data['processed_data'])} records added")
                f.write("\n\n")
            return True
        except Exception as exc:
            print(exc)
            return False
