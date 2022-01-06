#!/bin/python3

"""
This script reads in per-game and advanced stats from the 2020-2021
NBA season. We used this year since it was the only complte season 
relatively uninterrupted ßby the COVID-19 pandemic in recent memory

Ian Richard Ferguson
"""


# ---- Imports
import pandas as pd
import numpy as np


# ---- Run script
standard = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2021_per_game.html')[0]
advanced = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2021_advanced.html')[0]


def cleanup_dataframe(DF):
    """
    
    """

    DF = DF[DF['Player'] != 'Player'].reset_index(drop=True)
    clean_vars = [x for x in DF.columns if 'Unnamed' not in x]

    DF = DF.loc[:, clean_vars]

    for var in clean_vars:
        try:
            DF[var] = pd.to_numeric(DF[var])
            mean_value = DF[var].mean()
            DF[var].fillna(value=mean_value, inplace=True)
        except:
            continue

    return DF


cleaned_df = []

for frame in [standard, advanced]:
    cleaned_df.append(cleanup_dataframe(frame))

output = pd.merge(cleaned_df[0], cleaned_df[1], how='left', on=['Player', 'Tm'])

clean_vars = [x for x in output.columns if '_y' not in x]

output = output.loc[:, clean_vars]

output.to_csv('../nba-stats-2021.csv')
