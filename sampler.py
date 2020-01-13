import pandas as pd

filename = 'BikePath-nongeo/data/201910-bluebikes-tripdata'

trips_df = pd.read_csv(filename + '.csv')

trips_df['starttime'] = pd.to_datetime(trips_df['starttime'])
trips_df['stoptime'] = pd.to_datetime(trips_df['stoptime'])
trips_df = trips_df.set_index(pd.DatetimeIndex(trips_df['starttime']))

print(trips_df.head())

trips_grouped = trips_df.groupby(pd.Grouper(key='starttime', freq='D'))

print(trips_grouped)

print(trips_grouped.size())

sampled = trips_grouped.apply(lambda x: x.sample(frac=0.03))

print(sampled)

sampled['starttime'] = sampled['starttime'].apply(lambda x: x.replace(day=1))
sampled['stoptime'] = sampled['stoptime'].apply(lambda x: x.replace(day=1))

# sampled['starttime']=sampled['starttime'].dt.time
# sampled['stoptime']=sampled['stoptime'].dt.time

print(sampled)

sorted_df = sampled.reset_index(drop=True).sort_values(['starttime'], ascending=True)

print(sorted_df)

sampled.to_csv(filename + '-sampled.csv')
