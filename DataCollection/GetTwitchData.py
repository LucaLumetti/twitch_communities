import pandas as pd
import requests
import json

def GetTopStreams(client_id, client_secret, first, lang=None):
    print('Getting a list of top live streams...')

    Headers = {'Client-ID': f'{client_id}', 'Authorization': f'Bearer {client_secret}'}

    url = f'https://api.twitch.tv/helix/streams?first={first}'
    if(lang != None):
        url += f'&language={lang}'
    r = requests.get(url, headers=Headers)
    raw = r.text.encode('utf-8')
    j = json.loads(raw)
    return j

def getCurrentViewersForChannel(channel):
    print(f'Getting viewers for {channel}...')
    r = requests.get('http://tmi.twitch.tv/group/user/'+ channel.lower() +'/chatters').json()
    if(r == ''): return None
    currentViewers = r['chatters']['vips'] + r['chatters']['viewers'] + r['chatters']['moderators']
    return pd.Series(currentViewers)

def GetDictOfStreamersAndViewers(j):
    print("Creating dictionary of streamers and viewers...")
    df = pd.DataFrame()
    streamers = [element['user_name'] for element in j['data']]
    for streamer in streamers:
        viewers = getCurrentViewersForChannel(streamer.lower())
        df[streamer] = viewers
    return df
