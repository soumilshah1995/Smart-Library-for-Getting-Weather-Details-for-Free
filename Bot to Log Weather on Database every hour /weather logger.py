import json
import requests
import sqlite3
import time
import datetime
import schedule



class Weather(object):
    def __init__(self):
        self.__headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
        }

    def __get_lat_lon(self,zipcode='06604'):

        """
        This is Private class Client dont have Access to this
        :param zipcode: Takes Zip Code
        :return: Lat and Long
        """
        self.__url_zip = 'https://api.promaptools.com/service/us/zip-lat-lng/get/'

        params = {
            'key': '17o8dysaCDrgv1c',
            'zip':zipcode
        }

        r = requests.get(url=self.__url_zip,headers=self.__headers,params=params)
        data = r.json()

        for x in data["output"]:
            return x["latitude"], x["longitude"]

    def weather_get(self,zip='06604'):
        """

        :param zip: Takes Zip code as String
        :return: Weather Information
        """

        lat, long = self.__get_lat_lon(zip)

        data = '{},{}'.format(lat,long)

        self.__url_weather = "https://api.weather.com/v2/turbo/vt1observation"

        params= {
            'apiKey': 'd522aa97197fd864d36b418f39ebb323',
            'format': 'json',
            'geocode': data,
            'language': 'en-US',
            'units':'e'
        }

        r2 = requests.get(url=self.__url_weather,headers=self.__headers,params=params)

        r2_data = r2.json()

        dew_point = r2_data["vt1observation"]["dewPoint"]
        feelsLike = r2_data["vt1observation"]["feelsLike"]
        humidity = r2_data["vt1observation"]["humidity"]
        observationTime = r2_data["vt1observation"]["observationTime"]
        temperature = r2_data["vt1observation"]["temperature"]
        visibility = r2_data["vt1observation"]["visibility"]
        windspeed = r2_data["vt1observation"]["windSpeed"]
        winddegree = r2_data["vt1observation"]["windDirDegrees"]
        winddirection = r2_data["vt1observation"]["windDirCompass"]

        return dew_point, \
               feelsLike, \
               humidity, \
               observationTime, \
               temperature, \
               visibility, \
               windspeed, \
               winddegree, \
               winddirection


def Database(Dewpoint, Feellike, Humidity, Observationtime, Temperature, Visiblity, Windspeed, Winddegree, Winddirection,date, time):

    print("Added to Datbase.........")

    Dewpoint_v = str(Dewpoint)
    Feellike_v = str(Feellike)
    Humidity_v = str(Humidity)
    Observationtime_v = str(Observationtime)
    Temperature_v = str(Temperature)
    Visiblity_v = str(Visiblity)
    Windspeed_v = str(Windspeed)
    Winddegree_v = str(Winddegree)
    Winddirection_v = str(Winddirection)
    date_v = str(date)
    time_v = str(time)


    conn = sqlite3.connect("Weather.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather
    (Dewpoint TEXT,
    Feellike TEXT,
    Humidity TEXT,
    Observationtime TEXT,
    Temperature TEXT,
    Visiblity TEXT,
    Windspeed TEXT,
    Winddegree TEXT,
    Winddirection TEXT,
    date TEXT, 
    time TEXT)""")

    cursor.execute("""INSERT INTO weather 
    (Dewpoint,
     Feellike, 
     Humidity, 
     Observationtime, 
     Temperature, 
     Visiblity, 
     Windspeed, 
     Winddegree, 
     Winddirection,
     date,
     time)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (Dewpoint_v,
                                                   Feellike_v,
                                                   Humidity_v,
                                                   Observationtime_v,
                                                   Temperature_v,
                                                   Visiblity_v,
                                                   Windspeed_v,
                                                   Winddegree_v,
                                                   Winddirection_v,
                                                   date_v,
                                                   time_v))

    conn.commit()
    cursor.close()
    conn.close()

def main():

    w = Weather()

    dewpoint, feellike, humidity, observationtime, \
    temperature, visiblity, windspeed, winddegree, \
    winddirection = w.weather_get(zip='06604')

    t = datetime.datetime.now()
    date = "{}/{}/{}".format(t.month,t.day,t.year)
    time = "{}:{}:{}".format(t.hour,t.minute,t.second)

    Database(dewpoint, feellike, humidity, observationtime,
             temperature, visiblity, windspeed, winddegree,
             winddirection,date,time)


if __name__ == "__main__":
    schedule.every(10).seconds.do(main)
    while True:
        schedule.run_pending()