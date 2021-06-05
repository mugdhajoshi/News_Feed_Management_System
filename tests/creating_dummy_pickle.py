import pickle
import pandas as pd


def store_data():
    # initializing data to be stored in db
    dictionary = {'symbol': ['MMM', 'ABT'],
                  'company': ['3M Company', 'Abbott Laboratories'],
                  'sector': ['Industrials', 'Health Care'],
                  'industry': ['Industrial Conglomerates', 'Health Care Equipment'],
                  'headquarters': ['Maplewood, Minnesota', 'North Chicago, Illinois']
                  }
    dataframe = pd.DataFrame(dictionary, columns=['symbol', 'company', 'sector', 'industry', 'headquarters'])
    dbfile = open('dummy_pickle', 'ab')
    pickle.dump(dataframe, dbfile)
    dbfile.close()


def load_data():
    dbfile = open('dummy_pickle', 'rb')
    dataframe = pickle.load(dbfile)
    dbfile.close()
    return dataframe


if __name__ == '__main__':
    store_data()
    data = load_data()
    print(data)
