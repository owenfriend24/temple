#!/usr/bin/env python

from pathlib import Path
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
import subprocess


def run_com(command):
    #print(f"Running command: {command}")
    subprocess.run(command, shell=True)
            
def format_motion_data(sub, base_dir, out_path):
    df = pd.DataFrame(columns = ['sub', 'task', 'run', 'tr', 'dvars', 'fd'])
    for run in range(1, 7, 1):
        task = 'arrow'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index+1
                fd = data['framewise_displacement'][index]
                dvars = data['std_dvars'][index]
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]
    for run in range(1, 5, 1):
        task = 'collector'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index+1
                fd = data['framewise_displacement'][index]
                dvars = data['std_dvars'][index]
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]
    for run in range(1, 3, 1):
        task = 'movie'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index+1
                fd = data['framewise_displacement'][index]
                dvars = data['std_dvars'][index]
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]

    df.to_csv(out_path + 'all_motion.csv')      

def plot_arrow(sub, base_dir, out_path):
    df = pd.read_csv(out_path + 'all_motion.csv')
    a_data = df[df['task'] == 'arrow']
    
    run_data = {}  # Dictionary to store run data

    for run in range(1, max(a_data.run.values) + 1, 1):
        run_data[run] = a_data[a_data['run'] == run]

    # Set a seaborn color palette
    sns.set_palette("viridis")
    
    for measure in ['fd', 'dvars']:
        plt.figure(figsize=(15, 8))
        c = 0
        
        for run_number, run in run_data.items():
            mn = round(np.mean(run[measure]), 3)
            sd = round(np.std(run[measure]), 3)
            
            if measure == 'fd':
                num_t = len(run[run[measure] > 0.5])
            elif measure == 'dvars':
                num_t = len(run[run[measure] > 1.5])
            
            a_t = round(num_t / len(run['tr']) * 100, 3)
            l = f'run{run_number}: m={mn}, sd={sd}, above_threshold={a_t}% ({num_t} TRs)'
            
            if a_t > 30:
                plt.plot(np.array(run['tr']), np.array(run[measure]), linestyle='-', linewidth=2, label=l, color='red')
            else:
                plt.plot(np.array(run['tr']), np.array(run[measure]), linestyle='-', linewidth=2, label=l)
                
            c += 1

        # Add labels and title
        plt.xlabel('TR', fontsize=14)
        
        if measure == 'dvars':
            plt.ylabel('Standardized DVARS Value', fontsize=14)
            plt.title(f'Arrow: Sub {sub} - DVARS', fontsize=20)
            plt.axhline(y=1.5, color='r', linestyle='-')
        elif measure == 'fd':
            plt.ylabel('Framewise Displacement', fontsize=14)
            plt.title(f'Arrow: Sub {sub} - Framewise Displacement', fontsize=20)
            plt.axhline(y=0.5, color='r', linestyle='-')
        
        plt.xticks(df['tr'], fontsize=10)
        plt.yticks(fontsize=12)
        major_locator = MultipleLocator(base=10)
        plt.gca().xaxis.set_major_locator(major_locator)
        plt.xlim(0, 104)
        plt.legend(fontsize=16)
        
        # Save the plot
        plt.tight_layout()
        plt.grid(True)
        plt.savefig(out_path + f'{sub}-arrow-{measure}.png')
        
        
        
def plot_collector(sub, base_dir, out_path):
    df = pd.read_csv(out_path + 'all_motion.csv')
    a_data = df[df['task'] == 'collector']
    
    run_data = {}  # Dictionary to store run data

    for run in range(1, max(a_data.run.values) + 1, 1):
        run_data[run] = a_data[a_data['run'] == run]

    # Set a seaborn color palette
    sns.set_palette("viridis")
    
    for measure in ['fd', 'dvars']:
        plt.figure(figsize=(15, 8))
        c = 0
        
        for run_number, run in run_data.items():
            mn = round(np.mean(run[measure]), 3)
            sd = round(np.std(run[measure]), 3)
            
            if measure == 'fd':
                num_t = len(run[run[measure] > 0.5])
            elif measure == 'dvars':
                num_t = len(run[run[measure] > 1.5])
            
            a_t = round(num_t / len(run['tr']) * 100, 3)
            l = f'run{run_number}: m={mn}, sd={sd}, above_threshold={a_t}% ({num_t} TRs)'
            
            if a_t > 30:
                plt.plot(np.array(run['tr']), np.array(run[measure]), linestyle='-', linewidth=2, label=l, color='red')
            else:
                plt.plot(np.array(run['tr']), np.array(run[measure]), linestyle='-', linewidth=2, label=l)
            c += 1

        # Add labels and title
        plt.xlabel('TR', fontsize=14)
        
        if measure == 'dvars':
            plt.ylabel('Standardized DVARS Value', fontsize=14)
            plt.title(f'Collector: Sub {sub} - DVARS', fontsize=20)
            plt.axhline(y=1.5, color='r', linestyle='-')
        elif measure == 'fd':
            plt.ylabel('Framewise Displacement', fontsize=14)
            plt.title(f'Collector: Sub {sub} - Framewise Displacement', fontsize=20)
            plt.axhline(y=0.5, color='r', linestyle='-')
        
        plt.xticks(df['tr'], fontsize=10)
        plt.yticks(fontsize=12)
        major_locator = MultipleLocator(base=10)
        plt.gca().xaxis.set_major_locator(major_locator)
        plt.xlim(0, 150)
        plt.legend(fontsize=16)
        
        # Save the plot
        plt.tight_layout()
        plt.grid(True)
        plt.savefig(out_path + f'{sub}-collector-{measure}.png')

        
def plot_movie(sub, base_dir, out_path):
    df = pd.read_csv(out_path + 'all_motion.csv')
    a_data = df[df['task'] == 'movie']
    
    run_data = {}  # Dictionary to store run data

    for run in range(1, max(a_data.run.values) + 1, 1):
        run_data[run] = a_data[a_data['run'] == run]

    # Set a seaborn color palette
    sns.set_palette("viridis")
    
    for measure in ['fd', 'dvars']:
        plt.figure(figsize=(15, 8))
        c = 0
        
        for run_number, run in run_data.items():
            mn = round(np.mean(run[measure]), 3)
            sd = round(np.std(run[measure]), 3)
            
            if measure == 'fd':
                num_t = len(run[run[measure] > 0.5])
            elif measure == 'dvars':
                num_t = len(run[run[measure] > 1.5])
            
            a_t = round(num_t / len(run['tr']) * 100, 3)
            l = f'run{run_number}: m={mn}, sd={sd}, above_threshold={a_t}% ({num_t} TRs)'
            
            if a_t > 30:
                plt.plot(np.array(run['tr']), np.array(run[measure]), linestyle='-', linewidth=2, label=l, color='red')
            else:
                plt.plot(np.array(run['tr']), np.array(run[measure]), linestyle='-', linewidth=2, label=l)
            c += 1

        # Add labels and title
        plt.xlabel('TR', fontsize=14)
        
        if measure == 'dvars':
            plt.ylabel('Standardized DVARS Value', fontsize=14)
            plt.title(f'Movie: Sub {sub} - DVARS', fontsize=20)
            plt.axhline(y=1.5, color='r', linestyle='-')
        elif measure == 'fd':
            plt.ylabel('Framewise Displacement', fontsize=14)
            plt.title(f'Movie: Sub {sub} - Framewise Displacement', fontsize=20)
            plt.axhline(y=0.5, color='r', linestyle='-')
        
        plt.xticks(df['tr'], fontsize=10)
        plt.yticks(fontsize=12)
        major_locator = MultipleLocator(base=10)
        plt.gca().xaxis.set_major_locator(major_locator)
        plt.xlim(0, 200)
        plt.legend(fontsize=16)
        
        # Save the plot
        plt.tight_layout()
        plt.grid(True)
        plt.savefig(out_path + f'{sub}-movie-{measure}.png')
        
def main(data_dir, sub):
    base_dir = data_dir + f'/sub-{sub}/func/'
    out_dir = data_dir + '/motion/'
    run_com(f'mkdir {out_dir}sub-{sub}')
    out_path = out_dir + f'sub-{sub}/'

    format_motion_data(sub, base_dir, out_path)
    plot_arrow(sub, base_dir, out_path)
    plot_collector(sub, base_dir, out_path)
    plot_movie(sub, base_dir, out_path)
    print('done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="data directory")
    parser.add_argument("sub", help="subject number")
    args = parser.parse_args()
    main(args.data_dir, args.sub)
