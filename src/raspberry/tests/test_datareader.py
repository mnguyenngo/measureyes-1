from utils.datareader import DataReader


def test_datareader():
    person_data_path = '../data/output/persons_1538161541.csv'
    face_data_path = '../data/output/faces_1538161541.csv'
    results = DataReader(face_data_path, person_data_path)
    assert min(results.x_axis_ts) == 1538161541
    assert results.x_axis_timeofday[0] == '19:05:41'

    row = {
        'startX': 100,
        'endX': 200
    }
    assert results.get_object_centroid(row) == 150
