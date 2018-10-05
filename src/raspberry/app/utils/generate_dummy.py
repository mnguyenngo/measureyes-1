import numpy as np
import math
import scipy.stats as scs
import time

from .datahandler import DataHandler


def generate_dummy(duration, rate_person, rate_face, framerate):
    """Generate dummy data and write to a csv file

    Data will have one peak every 4 hours

    Arguments:
        duration (int): time in hours
        rate_person (int): average rate of persons detected per hour
        rate_faces (int): average rate of faces detected per hour
        framerate (int): frames per second

    Usage:
        dummy_results = DataHandler(measure='faces', path='../data/output',
                                    method='csv')
        dummy_results.generate_dummy(12, 600, 100, 8)
    """
    path = "../data/output"
    person_data = DataHandler(measure='persons', path=path, method='csv')
    face_data = DataHandler(measure='faces', path=path, method='csv')
    person_data.makefile()
    face_data.makefile()

    p_person = rate_person / 3600
    p_face = rate_face / rate_person
    p_frame = (framerate // 2 + 1) / framerate
    now = int(time.time())
    n = duration * 3600

    peak_multiplier = 4
    lull_multiplier = 0.25

    mults = get_multiplier_per_sec(n, peak_multiplier, lull_multiplier)

    # csv header
    # ts,label,id,confidence,startX,startY,endX,endY

    for idx, ts in enumerate(range(now, now+n, 1)):
        person_detected = scs.bernoulli(p=p_person*mults[idx]).rvs()
        if person_detected == 1:
            confidences = scs.binom(
                n=framerate, p=p_frame).rvs(framerate)/framerate
            for conf in confidences:
                person_data.write(
                    data=f"{ts},person,0,{conf},100,300,100,300")

            face_detected = scs.bernoulli(p=p_face).rvs()
            if face_detected == 1:
                confidences = scs.binom(
                    n=framerate, p=p_frame).rvs(framerate)/framerate
                for conf in confidences:
                    face_data.write(
                        data=f"{ts},face,0,{conf},100,300,100,300")

    person_data.close()
    face_data.close()


def get_multiplier_per_sec(n, peak_multiplier, lull_multiplier):
    period = n / 6 / math.pi
    peak_to_peak_amplitude = (peak_multiplier - lull_multiplier) / 2
    x = np.linspace(0, 6*period*math.pi, n)
    y = (peak_to_peak_amplitude * np.sin(x / period - math.pi/2) +
         (peak_to_peak_amplitude + lull_multiplier))
    return y
