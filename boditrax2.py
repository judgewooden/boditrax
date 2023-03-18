""" download Boditrax data to json or csv """
# pylint: disable=line-too-long
from http.cookiejar import CookieJar
import datetime
import random
import json
import pandas as pd
import requests
import browser_cookie3
import re
import time

class Boditrax2:
    """ Extract items into json """
    json_data = []
    items = ["Weight", "Muscle", "Fat", "Water", "Bone", "LegMuscleScore", "PhaseAngle", "FatFree", "VisceralFat", "MetabolicAge", "BasalMetabolicRate", "BMI"]

    def __init__( self, cookiejar: CookieJar = None):
        self.__fields: list = []
        self.__session = requests.Session()
        self.__session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
        })
        if cookiejar is not None:
            self.__session.cookies.update(cookiejar)
        else:
            for domain_name in ["boditrax.cloud", "member.boditrax.cloud"]:
                self.__session.cookies.update(browser_cookie3.load(domain_name=domain_name))

    def get_from_cloud(self, year=datetime.datetime.now().year ):
        """ load the data from the chart element on boditrax2 website """
        pattern = r"var\s+readings\s*=\s*JSON\.parse\(\s*'([^']*)'\s*\);"
        self.json_data = []
        for item in self.items:
            url = f'https://member.boditrax.cloud/Result/{item}/Track?year={year}'
            print(f"request: {url}")
            result = self.__session.get(url)
            if result.ok:
                if result.headers["Content-Type"].startswith("text/html;"):
                    match = re.search(pattern, result.content.decode("utf8"))
                    if match:
                        json_str = match.group(1)
                        readings = json.loads(json_str)
                        for d in readings:
                            d["category"] = item
                        self.json_data.extend(readings)
                    else:
                        raise Exception("readings not found")
                else:
                    raise Exception("Response not html")
            else:
                raise Exception(f"Status code: {result.status_code}")
            time.sleep(random.uniform(0.5, 2))

    def to_dataframe(self):
        """ convert the json to a dataframe"""
        df = pd.DataFrame(self.json_data)
        df = df.drop('id', axis=1)
        return df.pivot(index='date', columns='category', values='value')

if __name__ == "__main__":
    b = Boditrax2()
    b.get_from_cloud()
    df = b.to_dataframe()
    df.to_csv("boditrax2.csv")
