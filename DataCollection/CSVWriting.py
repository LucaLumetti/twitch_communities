import pandas as pd
import os
from pathlib import Path
import datetime

def UpdateTwitchData(df, data_dir):
    dir_path = Path().absolute()
    streamers = df.columns
    today = str(datetime.datetime.now())
    dir_path = f'{dir_path}/{data_dir}/{today}'
    os.makedirs(dir_path)
    for streamer in streamers:
        path = f'{dir_path}/{streamer}.csv'
        try:
            df[streamer].dropna().to_csv(path, index=False, header=False)
        except UnicodeError:
            print(f"Error for streamer {streamer}")
