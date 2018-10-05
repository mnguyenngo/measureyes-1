# Measureyes X Raspberry App

## Usage

The following script runs both object detection scripts at once.

```bash
$ python measure_faces.py -p models/deploy.prototxt.txt -m models/res10_300x300_ssd_iter_140000.caffemodel & python measure_persons.py -p models/MobileNetSSD_deploy.prototxt.txt -m models/MobileNetSSD_deploy.caffemodel
```

## Generating Dummy Data

Given:
600 persons per hour
  - 10 persons per minute
  - 1/6 probability a person is detected per second
  - each second, sample from a binomial distribution with p = 1/6
  - to generate the frame data, each frame will sample from a second binomial distribution with the following characteristics
    - p = (num_frames // 2 + 1) / num_frames
