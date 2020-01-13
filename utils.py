# https://www.tensorflow.org/api_docs/python/tf/edit_distance?version=stable
# start station, end station, start time, end time
# tf.edit_distance(
#     hypothesis,
#     truth,
#     normalize=True,
#     name='edit_distance'
# )

import pandas as pd
from holidays import US
import datetime


def clean_weather():
    filename = 'data/Bos Weather 2019'

    weather_df = pd.read_csv(filename + '.csv')
    weather_df['DATE'] = pd.to_datetime(weather_df['DATE'])

    weather_df = weather_df[weather_df['DATE'].dt.minute == 54]

    weather_df.loc[weather_df['HourlyPrecipitation']
        == 'T', 'HourlyPrecipitation'] = 0.0
    weather_df.loc[weather_df['HourlyPrecipitation']
        == '', 'HourlyPrecipitation'] = 0.0

    print(weather_df.head())

    weather_df.to_csv(filename + '.csv', index=False)


def add_holidays():
    filename = 'data/Bos Weather 2019'

    weather_df = pd.read_csv(filename + '.csv')
    weather_df['DATE'] = pd.to_datetime(weather_df['DATE'])

    def checkIfHoliday(x):
        x['holiday'] = (x['DATE'].date() in US())
        x['weekend'] = x['DATE'].weekday() >= 5
        return x

    weather_df = weather_df.apply(checkIfHoliday, axis=1)
    weather_df.to_csv(filename + '-holiday.csv', index=False)


def separate_weather_by_hour():
    filename = 'data/Bos Weather 2019'

    weather_df = pd.read_csv(filename + '-holiday.csv')
    weather_df['DATE'] = pd.to_datetime(weather_df['DATE'])

    def addHour(x):
        x['day'] = x['DATE'].date()
        x['hour'] = x['DATE'].time().hour
        return x

    weather_df = weather_df.apply(addHour, axis=1)
    weather_df.to_csv(filename + '-hour.csv', index=False)


def combine_weather():
    filename = 'data/201910-bluebikes-tripdata'

    trips_df = pd.read_csv(filename + '.csv')

    trips_df['starttime'] = pd.to_datetime(trips_df['starttime'])
    trips_df['stoptime'] = pd.to_datetime(trips_df['stoptime'])

    weather_df = pd.read_csv('data/Bos Weather 2019-hour.csv')
    weather_df['day'] = pd.to_datetime(weather_df['day'])

    def addHour(x):
        try:
            x['HourlyDewPointTemperature'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyDewPointTemperature'].iloc[0]
            x['HourlyDryBulbTemperature'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyDryBulbTemperature'].iloc[0]
            x['HourlyPrecipitation'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyPrecipitation'].iloc[0]
            x['HourlyRelativeHumidity'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyRelativeHumidity'].iloc[0]
            x['HourlyStationPressure'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyStationPressure'].iloc[0]
            x['HourlyVisibility'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyVisibility'].iloc[0]
            x['HourlyWindDirection'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyWindDirection'].iloc[0]
            x['HourlyWindSpeed'] = weather_df[(weather_df['day'] == x['starttime'].date()) & (
                weather_df['hour'] == x['starttime'].time().hour)]['HourlyWindSpeed'].iloc[0]
            x['holiday'] = weather_df[(weather_df['day'] == x['starttime'].date())]['holiday'].iloc[0]
            x['weekend'] = weather_df[(weather_df['day'] == x['starttime'].date())]['weekend'].iloc[0]
            print("combined", x.name)
        except:
            print("failed", x.name)
            pass
        return x
    
    print('combining')
    trips_df = trips_df.apply(addHour, axis=1)
    print('saving')
    trips_df.to_csv(filename + '-weather.csv', index=False)

def combine_holiday():
    filename = 'data/201910-bluebikes-tripdata-weather'

    trips_df = pd.read_csv(filename + '.csv')

    trips_df['starttime'] = pd.to_datetime(trips_df['starttime'])
    trips_df['stoptime'] = pd.to_datetime(trips_df['stoptime'])

    weather_df = pd.read_csv('data/Bos Weather 2019-hour.csv')
    weather_df['day'] = pd.to_datetime(weather_df['day'])
    
    def addHour(x):
        try:
            x['holiday'] = weather_df[weather_df['day'] == x['starttime'].date()]['holiday'].iloc[0]
            x['weekend'] = weather_df[weather_df['day'] == x['starttime'].date()]['weekend'].iloc[0]
        except:
            print("failed", x.name)
            pass
        return x
    
    print('combining')
    trips_df = trips_df.apply(addHour, axis=1)
    print('saving')
    trips_df.to_csv(filename + '-holiday.csv', index=False)

def data_cleaning():
    filename = 'data/201910-bluebikes-tripdata-small'

    trips_df = pd.read_csv(filename + '.csv')

    trips_df['starttime'] = pd.to_datetime(trips_df['starttime'])
    trips_df['stoptime'] = pd.to_datetime(trips_df['stoptime'])
    trips_df = trips_df.set_index(pd.DatetimeIndex(trips_df['starttime']))

    print(trips_df.head())

    trips_grouped = trips_df.groupby(pd.Grouper(key='starttime', freq='D'))

    print(trips_grouped.head(), )

# clean_weather()

# add_holidays()

# separate_weather_by_hour()

# combine_weather()

combine_holiday()

# data_cleaning()
