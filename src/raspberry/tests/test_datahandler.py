import unittest as unittest
from utils.datahandler import DataHandler


class Test(unittest.TestCase):
    def test_init(self):
        path_to_data_dir = "../data/output"
        results = DataHandler(measure="persons", path=path_to_data_dir,
                              method='csv')
        assert results.method == "csv"


if __name__ == '__main__':
    unittest.main()
