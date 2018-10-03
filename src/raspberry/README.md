# Raspberry Pi Documentation

## Documentation

* [OpenCV](https://docs.opencv.org/3.4/)
* [Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/)


## General Installation

### Setup on your computer

I used the [tutorial](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/) at pyimagesearch. I highlight some of the important steps when installing Python and OpenCV on the Raspberry Pi.

#### Download Raspbian Stretch and Load the image on a memory card

1. Download the ZIP file for RASPBIAN STRETCH WITH DESKTOP (1.6 GB)
[Download Link](https://www.raspberrypi.org/downloads/raspbian/)

2. Copy the Raspbian Stretch image to the microSD card.
https://howchoo.com/g/ndg2mtbmnmn/how-to-install-raspbian-stretch-on-the-raspberry-pi

  Optional: Add ssh file to the /Volumes/boot directory to enable ssh

3. Eject microSD

4. Load microSD into Raspberry Pi unit

5. Plug in keyboard and monitor

6. Plug into power. The Pi will now turn on and boot up.


### Setup on the Raspberry Pi

For the following steps, I followed the tutorial closely because all of the steps were laid out and easy to follow. I initially intended to include all of the syntax for the installation, but the tutorial already does a good job.

#### Initial setup

#### Update Packages

#### Download OpenCV
- OpenCV version: ____ (9/15/2018)

#### Download and Setup Python

#### Compile and Install OpenCV

- Configuring swap size: this was a new concept to me and is an important step to the installation. If you skip these steps, then the installation might stall during the process.

#### Testing the OpenCV Installation

- Changing swap size back

## HTR Detection

### Face Detector in OpenCV's Repo

There is a out-of-the-box face detector available in OpenCV:
* https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector

However:
> When using OpenCV’s deep neural network module with Caffe models, you’ll need two sets of files:
>
> * The .prototxt file(s) which define the model architecture (i.e., the layers themselves)
> * The .caffemodel file which contains the weights for the actual layers
>
> Both files are required to when using models trained using Caffe for deep learning.

Get the prototxt and caffemodel from the Google Drive and download the files to the Raspberry Pi:
* https://drive.google.com/drive/folders/16b2jIEeyvS_XowS-bzvOSTF3QJYw1al9?usp=sharing

#### Using OpenCV on macOS

* [Install OpenCV](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)
* Create a virtual environment. I made the virtual environment in the directory `measureyes/src/raspberry`. The env directory will be gitignored but I will update the requirements.txt file as I make progress.

```bash
virtualenv env
source env/bin/activate
```

* If you are cloning this repo and want to recreate the virtual environment:

```bash
pip install -r requirements.txt
```

#### Detecting Faces
Reference:
* https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/

In the face_detect directory:

```bash
python detect_faces_video.py --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel
```

#### Detect Persons
Reference:
* https://www.pyimagesearch.com/2017/10/16/raspberry-pi-deep-learning-object-detection-with-opencv/
* https://www.pyimagesearch.com/2018/05/14/a-gentle-guide-to-deep-learning-object-detection/
In the realtime_object_detect directory:

```bash
python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
```

#### Running two scripts at the same time
```bash
python face_detect/detect_faces_video.py --prototxt face_detect/deploy.prototxt.txt --model face_detect/res10_300x300_ssd_iter_140000.caffemodel & python realtime_object_detect/real_time_object_detection.py --prototxt realtime_object_detect/MobileNetSSD_deploy.prototxt.txt --model realtime_object_detect/MobileNetSSD_deploy.caffemodel
```

__press 'q' to quit__

__The script above will write data to two separate files__

#### Training a custom model to detect persons and faces at the same time


## Camera Installation with Raspberry Pi
Reference: https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

## Real Time Object Detection
Reference: https://www.pyimagesearch.com/2017/09/18/real-time-object-detection-with-deep-learning-and-opencv/

### Detecting Faces and Persons Only
Reference:
* https://www.pyimagesearch.com/2018/05/14/a-gentle-guide-to-deep-learning-object-detection/
* http://cocodataset.org/#home
* http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/

#### Method 1: Run person_detect and face_detect at the same time
We would have to analyze two different data files and infer if the person in view achieved a head-turn. This assumes we can write the data to a file.



## Next steps

- [ ] Connecting to Raspberry Pi using ssh

- [ ] InstallingTensorFlow Lite
