import unittest
from datetime import datetime
from pymongo import MongoClient


class TestMongo(unittest.TestCase):

    def setUp(self):
        client = MongoClient('localhost', 27017)
        mydatabase = client['test_database']
        self.mycollection = mydatabase['test_collection']
        self.item = {
            'security': None,
            'current_date': None,
            'author': None,
            'story_date': None,
            'story_time': None,
            'body': None,
            'title': None,
            'source': None
        }

    def test1_one_record_inserted(self):
        self.item['story_date'] = datetime.now().strftime("%d:%m:%Y")
        self.item['story_time'] = datetime.now().strftime("%H:%M:%S")
        inserted_id = self.mycollection.insert_one(self.item).inserted_id
        result = self.mycollection.find_one({'_id': inserted_id})
        self.assertNotEqual(result, [])

    def test2_one_record_data_matches(self):
        self.item['story_date'] = datetime.now().strftime("%d:%m:%Y")
        self.item['story_time'] = datetime.now().strftime("%H:%M:%S")
        inserted_id = self.mycollection.insert_one(self.item).inserted_id
        result = self.mycollection.find_one({'_id': inserted_id})
        self.assertEqual(result['story_date'], self.item['story_date'])


if __name__ == "__main__":
    unittest.main()
