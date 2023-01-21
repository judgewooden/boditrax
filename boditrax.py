""" download Boditrax data to json or csv """
# pylint: disable=line-too-long
from http.cookiejar import CookieJar
import datetime
import json
import pandas as pd
import requests
import browser_cookie3

class Boditrax:
    """
        This class will hold the variables from the server
        self._fields is a list of the variables
    """

    def __init__( self, cookiejar: CookieJar = None):
        self._fields: list = []

        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
        })
        if cookiejar is not None:
            self._session.cookies.update(cookiejar)
        else:
            for domain_name in ["boditrax.com", "cp.boditrax.com"]:
                self._session.cookies.update(browser_cookie3.load(domain_name=domain_name))

    def load_from_string(self, json_string: str):
        """ Load data from json string """
        for key, value in json.loads(json_string).items():
            setattr(self, key, value)
            self._fields.append(key)

    def load_from_file(self, filename: str):
        """ Load data from json file """
        with open(filename, encoding='utf-8') as file:
            self.load_from_string(file.read())

    def save_to_file(self, filename: str):
        """ Save data to a json file """
        items = {}
        for item in self._fields:
            items[item] = getattr(self, item)
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(items, file, sort_keys=False, indent=2)

    def to_dataframe(self):
        """ return self as a dataframe sorted by date """
        result = pd.DataFrame(columns=['date'])
        result['date'] = pd.to_datetime(result['date'])
        result.set_index('date', inplace=True)

        for item in self._fields:
            element = getattr(self, item)
            new = []
            for key, value in element['data']:
                date = datetime.datetime.fromtimestamp(key)
                new.append({"date": date, item: float(value)})
            df_temp = pd.DataFrame.from_records(new, columns =['date', item])
            df_temp['date'] = pd.to_datetime(df_temp['date'])
            df_temp.set_index('date', inplace=True)
            result = pd.concat([df_temp, result], axis=1)
        return result

    def get_from_cloud(self):
        """ load the data from the chart element on boditrax website """
        result = self._session.get('https://cp.boditrax.com/dashboard/track/lines')
        if result.ok:
            if result.headers["Content-Type"].startswith("application/json"):
                self.load_from_string(result.content.decode("utf8"))
            else:
                raise Exception("Response not json")
        else:
            raise Exception(f"Status code: {result.status_code}")


if __name__ == "__main__":
    b = Boditrax()
    b.get_from_cloud()
    # b.load_from_file(filename='lines5.json')
    # b.save_to_file(filename='output.json')
    df = b.to_dataframe()
    df.to_csv("boditrax.csv")

    # print("FIELDS:", b._fields)
    # print("LENGTH", len(df))

    # print(b.fatpercentage['name'])
    # print(b.fatpercentage['primaryUnit'])
    # print(b.fatpercentage)

    print(df.tail())
