import sys
import csv
import pandas as pd
import os
from itertools import combinations
import functools
from pathlib import Path

VIEWS_THRESHOLD = 0
OVERLAP_THRESHOLD = 5

@functools.lru_cache(None)
def LoadStreamerViewers(streamer):
    v = pd.read_csv(f"../DataCollection/data/{streamer}.csv", names=['username','n'])
    v = v[v['n'] > VIEWS_THRESHOLD]['username']
    if(len(v) < OVERLAP_THRESHOLD): return set()
    return set(v)

def CreateOverlapDict(streamers):
    overlaps = {}
    combo = combinations(streamers,2)

    print(f"Combining {len(streamers)} streamers...")
    for s1,s2 in combo:
        v1 = LoadStreamerViewers(s1)
        v2 = LoadStreamerViewers(s2)

        overlap = len(v1 & v2)
        if overlap < OVERLAP_THRESHOLD: continue
        print(f"{s1} and {s2} have {overlap} viewers in common")
        if s1 not in overlaps: overlaps[s1] = {}
        if s2 not in overlaps[s1]: overlaps[s1][s2] = {}
        overlaps[s1][s2] = overlap
    return overlaps

def GenerateGephiData(dict):
    dir_path = Path().absolute()
    data_path = f'{dir_path}/gephi/Data.csv'
    with open(data_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Source", "Target", "Weight"])
        for key, value in dict.items():
            nodeA = key
            for node, count in value.items():
                nodeB = node
                writer.writerow([nodeA, nodeB, count])

def GenerateGephiLabels(streamers):
    dir_path = Path().absolute()
    labels_path = f'{dir_path}/gephi/Labels.csv'
    print("Generating Labels...")
    with open(labels_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Label", "Count"])
        for s in streamers:
            v = set(open(f'{dir_path}/../DataCollection/data/{s}.csv').read().splitlines())
            writer.writerow([s, s, len(v)])

print("Reading streamers")
dir_path = Path().absolute()
streamers = [ f.replace('.csv','') for f in os.listdir(f'{dir_path}/../DataCollection/data') ]
print("Creating overlap dict")
d = CreateOverlapDict(streamers)
GenerateGephiData(d)
GenerateGephiLabels(streamers)
