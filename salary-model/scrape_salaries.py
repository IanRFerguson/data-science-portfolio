#!/bin/python3

"""
About this Script

We'll read in players stats and salaires from 
Basketball Reference, merge them into one DataFrame,
and save as a local CSV for modeling in R

Ian Richard Ferguson | Stanford University
"""

# ---- Imports + Setup
import pandas as pd


# Read in Salary data from Basketball Reference
salaries = pd.read_html("https://www.basketball-reference.com/contracts/players.html")[0]
players = pd.read_html("https://www.basketball-reference.com/leagues/NBA_2020_totals.html")[0]


# ---- Data cleaning
salary_clean = []

for k in salaries.columns:

    if len(k) > 1:
        salary_clean.append(k[1])

    else:
        salary_clean.append(k)

salaries.columns = salary_clean                                         # Remove extra column headers + replace with cleaned text
salaries = salaries.loc[:, ["Player", "2019-20"]]                       # Chop down extraneous columns
salaries.columns = ["Player", "Salary"]                                 # Rename remaining columns
total = pd.merge(left=players, right=salaries, on="Player")             # Combine stats + salaries
total = total[total["Player"] != "Player"]                              # Toss extraneous lines

# ---- Push to local CSV
total.to_csv("Stats-and-Salaries.csv", index=False)                     # Push DataFrame to CSV