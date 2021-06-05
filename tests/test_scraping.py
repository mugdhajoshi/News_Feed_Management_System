import unittest
from selenium import webdriver
import sys
sys.path.append('..')
import generate_url
import news_scrapper
import pymongo


class SeleniumTest(unittest.TestCase):

    def setUp(self):
        chrome_driver = 'C:\\Users\\mugdh\\Downloads\\chromedriver.exe'
        self.driver = webdriver.Chrome(chrome_driver)
        self.symbol = ['MMM']
        self.all_urls = []

    def test1_deserialize(self):
        self.symbol = generate_url.deserialize('C://Users//mugdh//PycharmProjects//intellimind//tests//dummy_pickle')
        self.assertIsNotNone(self.symbol)
        self.assertIsInstance(self.symbol, list)

    def test2_generate_url(self):
        for s in self.symbol:
            urls = generate_url.generate_url(s)
            self.all_urls.append(urls)
            self.assertIsNotNone(urls)

    def test3_connection_to_mongodb(self):
        collection = news_scrapper.connection_to_mongodb()
        self.assertIsInstance(collection, pymongo.collection.Collection)


if __name__ == "__main__":
    unittest.main()
