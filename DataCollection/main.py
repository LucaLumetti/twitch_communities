import GetTwitchData
import CSVWriting
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('client_id', help='client id from twitchtokengenerator.com')
parser.add_argument('client_secret', help='client secret token from twitchtokengenerator.com')
parser.add_argument('--data_dir', default='data', help='directory where data is stored or need to be stored')
parser.add_argument('--top', default=100, help='how many streamers to parse')
parser.add_argument('--lang', default=None, help='language of the streamers')
args = parser.parse_args()

json = GetTwitchData.GetTopStreams(args.client_id, args.client_secret, args.top, args.lang)
df = GetTwitchData.GetDictOfStreamersAndViewers(json)
CSVWriting.UpdateTwitchData(df, args.data_dir)
