#!/bin/python3

"""
About this Script

Scrapes and aggregates salary and player data for the 2021-2022 season

Ian Richard Ferguson
"""


# ---- Imports + Setup
import pandas as pd

# Pool of URLs to read in as DataFrame objects
urls = ['https://www.basketball-reference.com/contracts/players.html',
        'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html',
        'https://www.basketball-reference.com/leagues/NBA_2022_advanced.html']


def clean_df(DF):
      return DF[DF['Player'] != 'Player'].reset_index(drop=True)


# ---- Salary data
salaries = pd.read_html(urls[0])[0]                                                             # Read in Salary data
salaries.columns = [x[1].strip() for x in salaries.columns]                                     # Eliminate MultiIndex column names
salaries = salaries[salaries['Player'] != 'Player'].reset_index(drop=True).iloc[:, 1:4]         # Remove check rows
salaries = salaries[salaries['2021-22'] != 'Salary'].reset_index(drop=True)                     # ^^


# ---- On-court data
per_game = pd.read_html(urls[1])[0]                                                             # Read in per-game stats
advanced = pd.read_html(urls[2])[0]                                                             # Read in advanced stats

per_game, advanced = clean_df(per_game), clean_df(advanced)                                     # Apply clean_df() function
nba = per_game.merge(advanced, on=['Player', 'Tm'], how='inner')                                # Combine per_game and advanced

clean_columns = [x for x in nba.columns if '_y' not in x if 'Unnamed' not in x]                 # Remove extra columns
nba = nba.loc[:, clean_columns]                                                                 # Subset dataframe

clean_columns = [x.replace('_x', '') for x in nba.columns]                                      # Remove trailing characters
nba.columns = clean_columns                                                                     # Clean column names


# -- Isolate individual player data
total_players = nba[nba['Tm'] == 'TOT'].reset_index(drop=True)                                  # Remove traded players
players_to_drop = list(total_players['Player'])                                                 # List of traded player names

nba = nba[~nba['Player'].isin(players_to_drop)].reset_index(drop=True)                          # Remove traded players from master DF
nba = pd.concat([nba, total_players]).sort_values(by='Player').reset_index(drop=True)           # Add traded players back into df


# ---- Merge all data
nba = nba.merge(salaries, on='Player', how='left')                                              # Combine stats and salaries
nba = nba.drop_duplicates().reset_index(drop=True).rename(columns={'2021-22':'Salary'})         # Drop duplicate rows
nba = nba[~nba['Salary'].isna()].drop(columns=['Tm_y'])                                         # Drop missing salary values

# ---- Push to local CSV
nba.to_csv('./advanced_stats_and_salaries.csv', index=False)