import numpy as np
import pandas as pd
from pathlib import Path

data = Path('data/india')
processed = Path('data/processed')

df = pd.read_csv(Path(data, 'constellationship.fab'), header=None)
# Manually process the lines and build the dataframe because the format is a bit weird
df['constellation'] = df[0].str.split().str.get(0)
# print(df.constellation)
df['num_pairs'] = df[0].str.split().str.get(1)
df['stars'] = df[0].str.split().str[2:]
df.drop(0, axis=1, inplace=True)  # Drop the original column
# print(df)
# print(len(df))

# Needed to remove two trailing tabs in the data...
df_names = pd.read_csv(Path(data, 'constellation_names.eng.fab'), header=None, comment='#', sep='\t', names=['constellation', 'san', 'eng'])
df_names['eng'] = [x.split('"')[1] for x in df_names['eng']]
# print(df_names)
# print(len(df_names))

# assert len(df) == len(df_names)
# df has one more row: constellation named C01

df = pd.merge(df, df_names, on="constellation")
# print(df.head())



stars = [float(y) for x in df['stars'].tolist() for y in x]
stars = sorted(set(stars))

# print(len(stars))  # 278 stars


# Load StarID, Right Ascension and Declination from our processed HYG data.
hip_df = pd.read_csv(Path(processed, 'hygdata_v37_processed.csv'), low_memory=False)
# Select and rename columns using a dictionary
selector_d = {'hip':'star_ID', 'ra':'ra', 'dec':'dec'}
star_df = hip_df[hip_df['hip'].isin(stars)][[*selector_d]].rename(columns=selector_d)
# print(len(star_df))

df['ra'] = ''
df['dec'] = ''
for idx, row in df.iterrows():
	ras, decs = [], []
	for s in row['stars']:
		ras.append(star_df[star_df['star_ID']==float(s)]['ra'].values[0])
		decs.append(star_df[star_df['star_ID']==float(s)]['dec'].values[0])
	df.at[idx, 'ra'] = ras
	df.at[idx, 'dec'] = decs

# print(df.head())

zodiacs = ['Meṣa Rāśi', 'Vṛṣa Rāśi', 'Mithuna Rāśi', 'Karkaṭa Rāśi', 'Simha Rāśi', 'Kanyā Rāśi', 'Tulā Rāśi', 
           'Vṛścikā Rāśi', 'Dhanur Rāśi', 'Makara Rāśi', 'Kumbha Rāśi', 'Mīna Rāśi']
df['zodiac'] = df['san'].isin(zodiacs)
assert df['zodiac'].sum() == 12
print(df.head())
df.to_csv(Path(processed, 'asterisms.csv'), index=False)