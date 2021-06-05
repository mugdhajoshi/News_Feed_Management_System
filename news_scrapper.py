# Importing the required libraries
from generate_url import generate_url, deserialize
from selenium import webdriver
from datetime import datetime
from dateutil import tz
from pymongo import MongoClient
import pymongo
from multiprocessing import Pool
from typing import Dict, List, Tuple


def convert_utc_to_ist(utc: str) -> Tuple:
    """
    Function to convert UTC to IST and return date and time as tuple

    Converting UTC time to IST
    :param utc: String which contain time in UTC
    :return: tuple of date and time converted to IST
    """

    # Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Convert string to datetime object
    utc = datetime.strptime(utc, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)

    # return date and time as tuple
    return (central.strftime("%d-%m-%Y"), central.strftime("%H:%M:%S"))


def connection_to_mongodb():
    # Creating Connection to MongoDB collection
    client = MongoClient('localhost', 27017)
    mydatabase = client['news_intellimind']
    mycollection = mydatabase['collection']
    return mycollection


def news_parser(driver: webdriver.chrome.webdriver.WebDriver,
                all_urls: List[Dict[str, List[str]]],
                mycollection: pymongo.collection.Collection) -> None:

    """
    Function to scrape the news from the links and store it in MongoDB

    :param driver: Selenium webdriver
    :param all_urls: List of Dictionary of symbol and list of their news URL
    :param mycollection: collection object
    :return: None
    """

    # Traversing in all the URl's
    for a in all_urls:
        for symbol, value in a.items():
            for link in value:
                try:

                    # Open the link in chrome webdriver
                    driver.get(link.strip("'"))

                    # Scraping the various fields
                    source = driver.find_element_by_xpath(
                        '//span[@class="caas-attr-provider caas-attr-item caas-attr-show-provider"]').text
                    author = driver.find_element_by_xpath('//div[@class="caas-attr-meta"]').text
                    author = author.split("\n")[0]
                    if '-min read' in author:
                        author = None
                    title = driver.find_element_by_xpath('//header[@class="caas-title-wrapper"]/h1').text
                    body = driver.find_element_by_xpath('//div[@class="caas-body"]').text
                    date_time = driver.find_element_by_xpath('//div[@class="caas-attr-time-style"]')
                    date_time_combined = date_time.find_element_by_tag_name('time').get_attribute('datetime')

                    # Scraped time is in UTC therefore calling the function to convert in IST
                    story_date, story_time = convert_utc_to_ist(date_time_combined)
                    current_date = datetime.now().strftime("%d-%m-%Y")
                    security = symbol

                    # Storing the Scraped data in MongoDB
                    mycollection.insert_one({'security': security, 'current_date': current_date, 'author': author,
                                             'story_date': story_date, 'story_time': story_time, 'body': body,
                                             'title': title,
                                             'source': source
                                             })
                except Exception:
                    print("Exception Occurred and handled")


def main():
    # Creating the new instance of google chrome
    chrome_driver = 'C:\\Users\\mugdh\\Downloads\\chromedriver.exe'
    driver = webdriver.Chrome(chrome_driver)

    # Storing all the symbol in symbol
    symbol = deserialize()

    # Parallel Execution for extracting URL's
    p = Pool(10)
    all_urls = p.map(generate_url, symbol)
    p.terminate()
    p.join()

    # Storing all the scraped URL in a file
    with open("all_url", "w") as file:
        file.write(str(all_urls))

    # Creating connection to Mongodb collection
    mycollection = connection_to_mongodb()

    # Calling the function that will scrape the URL's and store the scraped fields in MongoDB
    news_parser(driver, all_urls, mycollection)


if __name__ == "__main__":
    main()
