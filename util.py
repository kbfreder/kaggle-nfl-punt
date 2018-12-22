import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def pkl_this(filename, df):
    '''Saves df as filename. Must include .pkl extension'''
    with open(filename, 'wb') as picklefile:
        pickle.dump(df, picklefile)

def open_pkl(filename):
    '''Must include .pkl extension. Returns object that can be saved to a df.
    '''
    with open(filename,'rb') as picklefile:
        return pickle.load(picklefile)

def log_this(s):
    with open("log.txt", "a") as f:
        f.write("\n" + s + "\n")

def plot_player_speed(gid):
    df = ngs1[ngs1['GSISID'] == gid]
    xs = df['Time']
    plt.plot(xs, df['speed'], label='Speed')
    plt.plot(xs, df['accel'], label='Accel', alpha=0.4)
    plt.title(f'Player ID {gid}')
    plt.legend();

def calc_accel_play(gk, pid, ngs_df):
    ngs1 = ngs_df[(ngs_df['GameKey'] == gk) & (ngs_df['PlayID'] == pid)]
    ngs1 = ngs1.drop(columns=['GameKey', 'PlayID', 'Season_Year'])

    ngs1.reset_index(drop=True, inplace=True)

    ngs1['dt'] = ngs1.groupby('GSISID')['Time'].diff()
    ngs1['dt'] = ngs1['dt'].apply(lambda x: x.total_seconds())

    ngs1['dx'] = ngs1.groupby('GSISID')['x'].diff()
    ngs1['dy'] = ngs1.groupby('GSISID')['y'].diff()
    ngs1['dist'] = np.sqrt(ngs1['dx']**2 + ngs1['dy']**2) * 0.9144

    ngs1['speed'] = ngs1['dist'] / ngs1['dt']
    ngs1['d_speed'] = ngs1.groupby('GSISID')['speed'].diff()
    ngs1['accel'] = ngs1['d_speed'] / ngs1['dt']
    ngs1 = ngs1[ngs1['accel'] < 50]

    return ngs1


def calc_accel_ngs(filename):
    '''filename: NGS filename'''
    ngs1 = pd.read_csv(filename, parse_dates=['Time'])
    ngs1.sort_values(by='Time', ascending=True, inplace=True)
    ngs1.reset_index(drop=True, inplace=True)

    ngs1['dt'] = ngs1.groupby(['GameKey','PlayID','GSISID'])['Time'].diff()
    ngs1['dt'] = ngs1['dt'].apply(lambda x: x.total_seconds())

    ngs1['dx'] = ngs1.groupby(['GameKey','PlayID','GSISID'])['x'].diff()
    ngs1['dy'] = ngs1.groupby(['GameKey','PlayID','GSISID'])['y'].diff()
    ngs1['dist'] = np.sqrt(ngs1['dx']**2 + ngs1['dy']**2) * 0.9144

    ngs1['speed'] = ngs1['dist'] / ngs1['dt']
    ngs1['d_speed'] = ngs1.groupby(['GameKey','PlayID','GSISID'])['speed'].diff()
    ngs1['accel'] = ngs1['d_speed'] / ngs1['dt']

    return ngs1

def get_play_info(gk, pid):
    return pi[(pi['GameKey'] == gk) & (pi['PlayID'] == pid)]

def get_play_ngs(gk, pid, df):
    '''gk: GameKey
       pid: PlayID
       df: NGS dataframe'''
    new_df = df[(df['GameKey'] == gk) & (df['PlayID'] == pid)]
    new_df = new_df.drop(columns=['GameKey', 'PlayID', 'Season_Year'])
    return new_df

def plot_all_accels(play_df, inj_id=None):
    '''df: dataframe containing accel data for a single play'''
    plt.figure(figsize=(8,5))

    for x in play_df['GSISID'].unique():
        if x == inj_id:
            c = 'r'
            a = 0.8
        else:
            c = 'b'
            a = 0.2
        df = play_df[play_df['GSISID'] == x]
        plt.plot(df['Time'], df['accel'], label=x, color=c, alpha=a);
    return plt;
