import pandas as pd
from pathlib import Path

def UpdateTwitchData(df, data_dir):
    dir_path = Path().absolute()
    streamers = df.columns
    for streamer in streamers:
        path = f'{dir_path}/{data_dir}/{streamer}.csv'
        viewers = pd.DataFrame(columns=['username','n'])
        try:
            if(Path(path).exists()):
                viewers = pd.read_csv(path,names=['username','n'])
            viewers.loc[viewers['username'].isin(df[streamer]), 'n'] += 1

            new_viewers = df[streamer].isin(viewers['username']) == False
            new_viewers = pd.DataFrame({'username': df[streamer][new_viewers], 'n': 1}, columns=['username','n'])

            viewers = pd.DataFrame(pd.concat([viewers, new_viewers], axis=0))
            viewers.dropna().to_csv(path, index=False, header=False)
        except UnicodeError:
            print(f"Error for streamer {streamer}")
