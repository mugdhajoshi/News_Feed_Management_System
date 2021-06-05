# Importing the libraries
from multiprocessing import Pool
from typing import Dict, List
import pandas as pd
from selenium import webdriver


def deserialize(file_path: str = 'C://Users//mugdh//Downloads//symbols.pickle') -> List[str]:
    """
    Function to deserialize a pickle file containing security

    :param file_path: location of the pickle file which contain security and company name
    :return: list of all the company symbols
    """

    dataframe = pd.read_pickle(file_path)
    return list(dataframe.symbol)


def generate_url(symbol: str) -> Dict[str, List[str]]:
    """
    Function to generate all the URLs based on security

    :param symbol: symbol of company
    :return: List of Dictionary of symbol and list of their news URL
    """

    try:

        # Creating the new instance of google chrome
        chrome_driver = 'C:\\Users\\mugdh\\Downloads\\chromedriver.exe'
        driver = webdriver.Chrome(chrome_driver)

        all_urls: Dict[str, List[str]] = {}
        base_url = 'https://in.finance.yahoo.com/'
        all_urls[symbol] = []

        # Open the URL based on symbols
        driver.get(base_url + 'quote/' + str(symbol) + "?p=" + str(symbol) + "&.tsrc=fin-srch")

        # Getting the news link of a particular company
        list_of_news = driver.find_elements_by_xpath('//h3[@class="Mb(5px)"]')
        for el in list_of_news:
            anchor = el.find_element_by_tag_name('a')
            all_urls[symbol].append(anchor.get_attribute('href'))
        driver.quit()
    except Exception as e:
        print("Exception Occurred and handled")
        driver.quit()

    return all_urls


def main():

    # Storing all the symbol in symbol
    symbol = deserialize()

    # Parallel Execution for extracting URL's
    p = Pool(10)
    all_urls = p.map(generate_url, symbol)
    p.terminate()
    p.join()

    # Printing all the URLs
    print(all_urls)


if __name__ == "__main__":
    main()
