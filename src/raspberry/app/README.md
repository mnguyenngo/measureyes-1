# Measureyes X Raspberry App

## Usage

The following script runs both object detection scripts at once.

```bash
$ python measure_faces.py -p models/deploy.prototxt.txt -m models/res10_300x300_ssd_iter_140000.caffemodel & python measure_persons.py -p models/MobileNetSSD_deploy.prototxt.txt -m models/MobileNetSSD_deploy.caffemodel
```

## Streaming Data to Dashboard Web App

### Making a POST request for a JSON file
```bash
$ http POST https://hidden-lowlands-41791.herokuapp.com/responses/1 @me_data.json
```

### Starting the streaming script while object detection is running
```bash
$ python stream_to_dashboard.py -f <path to face data> -p <path to person_data> -a "https://hidden-lowlands-41791.herokuapp.com/response/1"
```

## Generating Dummy Data

Given:
600 persons per hour
  - 10 persons per minute
  - 1/6 probability a person is detected per second
  - each second, sample from a binomial distribution with p = 1/6
  - to generate the frame data, each frame will sample from a second binomial distribution with the following characteristics
    - p = (num_frames // 2 + 1) / num_frames
