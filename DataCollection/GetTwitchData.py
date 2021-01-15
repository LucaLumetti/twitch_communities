import pandas as pd
import requests
import json

#Gets the numberOfStreams top streams currently live on twitch. numberOfStreams max is 100
def GetTopStreams(client_id, client_secret, first, lang=None):
    print('Getting a list of top live streams...')

    #Header auth values taken from twitchtokengenerator.com, not sure what to do if they break
    Headers = {'Client-ID': f'{client_id}', 'Authorization': f'Bearer {client_secret}'}

    url = f'https://api.twitch.tv/helix/streams?first={first}'
    if(lang != None):
        url += f'&language={lang}'
    r = requests.get(url, headers=Headers)
    raw = r.text.encode('utf-8')
    j = json.loads(raw)
    return j

#Get the a list of viewers for a given twitch channel from tmi.twitch (Not an API call)
def getCurrentViewersForChannel(channel):
    print(f'Getting viewers for {channel}...')
    r = requests.get('http://tmi.twitch.tv/group/user/'+ channel.lower() +'/chatters').json()
    if(r == ''): return None
    currentViewers = r['chatters']['vips'] + r['chatters']['viewers'] + r['chatters']['moderators']
    return pd.Series(currentViewers)

#This method looks up the viewers of each streamer in j and creates a large dictionary of {streamer: [viewers]}
def GetDictOfStreamersAndViewers(j):
    print("Creating dictionary of streamers and viewers...")
    df = pd.DataFrame()
    streamers = [element['user_name'] for element in j['data']]
    for streamer in streamers:
        viewers = getCurrentViewersForChannel(streamer.lower())
        df[streamer] = viewers
    return df
