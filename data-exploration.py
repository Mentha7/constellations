import pandas as pd
import numpy as np

# Load dataframe directly from gzip file
df = pd.read_csv('data/hygdata_v37.csv.gz', compression='gzip', header=0, sep=',', quotechar='"')
print(df.head())

# Check all column names
print(df.columns.values)