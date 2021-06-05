import unittest
import requests


class TestApi(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:5000/'

    def test_1_base_url(self):
        r = requests.get(self.base_url)
        self.assertEqual(r.status_code, 200)

    def test_2_article_captured_by_source(self):
        count = self.base_url + "count_of_article_captured_by_source"
        r = requests.get(count)
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.content), 1)

    def test_3_article_captured_by_source_and_date(self):
        count = self.base_url + "count_of_article_captured_by_source_and_date"
        r = requests.get(count)
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.content), 1)


if __name__ == "__main__":
    unittest.main()
