import os
import re
import pandas as pd


class Preprocess:
    def __init__(self, name):
        self.city_name = name

    @staticmethod
    def get_processed_dfs(calendar_df, listings_df):
        """do the transformations"""
        return calendar_df, listings_df

    @staticmethod
    def parse_urls(links):
        return pd.DataFrame(
            {"link": links, 'country': [x.split('/')[3] for x in links], 'state': [x.split('/')[4] for x in links],
             'city': [x.split('/')[5] for x in links], 'type': [re.search(r'(\w*)\.csv', x)[1] for x in links]})


class City:
    def __init__(self, name, urls):
        parsed_urls = Preprocess.parse_urls(urls)
        self.name = name
        self.listings_url = parsed_urls.loc[(parsed_urls['type'] == 'listings') & (parsed_urls['city'] == name)].iloc[
            0].link
        self.calendar_url = parsed_urls.loc[(parsed_urls['type'] == 'calendar') & (parsed_urls['city'] == name)].iloc[
            0].link


class DataInterface:
    def __init__(self, name, storage_type='local', location=None):
        self.city = name
        self.storage_type = storage_type
        self.location = location

    def get_data(self):
        if self.storage_type == 'local':
            self.location = self.location if self.location is not None else f'./Data/{self.city.name}'
            return pd.read_csv(f'{self.location}/calendar.csv'), pd.read_csv(f'{self.location}/listings.csv')


    def put_data(self):
        pass


class ETL:
    def __init__(self, city, storage_type='local', storage_location=None):
        self.city = city
        self.storage_type = storage_type
        self.storage_location = storage_location
        self.calendar_df = None
        self.listings_df = None

    def extract(self):
        if self.storage_type == 'local':
            self.listings_df = pd.read_csv(self.city.listings_url)
            self.calendar_df = pd.read_csv(self.city.calendar_url)

    def transform(self):

        self.calendar_df, self.listings_df = Preprocess.get_processed_dfs(calendar_df=self.calendar_df,
                                                                          listings_df=self.listings_df)

    def load(self):
        if self.storage_type == 'local':
            self.storage_location = self.storage_location if self.storage_location is not None else f'./Data/{self.city.name}'
            os.makedirs(self.storage_location, exist_ok=True)
            self.calendar_df.to_csv(f'{self.storage_location}/calendar.csv')
            self.listings_df.to_csv(f'{self.storage_location}/listings.csv')



    def export_data_interface(self, tofile=False, path='.'):
        if tofile:
            import pickle
            dif = DataInterface(self.city.name, storage_type=self.storage_type, location=self.storage_location)
            pickle.dump(dif, open(f'{path}/DataInterface_{self.city.name}.obj', 'wb'))
        else:
            return DataInterface(self.city.name, storage_type=self.storage_type, location=self.storage_location)


if __name__ == '__main__':
    from bs4 import BeautifulSoup
    import requests

    url = "http://insideairbnb.com/get-the-data/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    links_scraped = []
    for link in soup.find_all('a'):
        if link.get('href') is not None:
            links_scraped.append(link.get('href'))
    links_scraped = [x for x in links_scraped if 'csv' in x]
    seattle = City('amsterdam', links_scraped)
    etl = ETL(seattle)
    etl.extract()
    etl.transform()
    etl.load()
    datainterface_amsterdam = etl.export_data_interface()
    print(datainterface_amsterdam.get_data())