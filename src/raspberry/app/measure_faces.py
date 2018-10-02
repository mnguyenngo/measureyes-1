"""Run webcam to detect faces and log data in a csv file

Source: This code was modified from code provided by PyImageSearch.

USAGE
>>> python measure_faces.py -p deploy.prototxt.txt -m res10_300x300_ssd_iter_140000.caffemodel

press 'q' to quit
"""

# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import plac
from utils.datahandler import DataHandler


@plac.annotations(
    prototxt=("path to Caffe 'deploy' prototxt file", "option", "p"),
    model=("path to Caffe pre-trained model", "option", "m"),
    min_confidence=("minimum probability to filter weak detections", "option",
                    "c"))
def main(prototxt, model, min_confidence=0.5):
    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

    # NN: open a csv file to write data; 'a' to append and not overwrite
    path_to_data_dir = "../data/output"
    results = DataHandler(measure="faces", path=path_to_data_dir, method='csv')

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < min_confidence:
                continue

            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255),
                          2)
            cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.45, (0, 0, 255), 2)

            # NN: write to output file
            now = int(time.time())
            data = "{},face,{},{:.2f},{},{},{},{}".format(
                now, i, confidence, startX, startY, endX, endY)
            results.write(data)

        # show the output frame
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # NN: close the results file
    results.close()

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()


if __name__ == '__main__':
    plac.call(main)
