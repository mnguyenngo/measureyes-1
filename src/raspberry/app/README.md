# Measureyes X Raspberry App

## Usage

The following script runs both object detection scripts at once.

```bash
$ python measure_faces.py -p models/deploy.prototxt.txt -m models/res10_300x300_ssd_iter_140000.caffemodel & python measure_persons.py -p models/MobileNetSSD_deploy.prototxt.txt -m models/MobileNetSSD_deploy.caffemodel
```
