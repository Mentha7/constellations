import numpy as np
import pandas as pd

from pathlib import Path

from logger import logger

'''
Data Source:
Manually curated using W.H. Finlay's Concise Catalog of Deep-sky Objects as reference (The CSV file contains
all objects in the book with magnitude < 6.5).

Download CSV from:
https://github.com/eleanorlutz/western_constellations_atlas_of_space/blob/main/data/messier_ngc.csv
'''

data = Path('data')
processed = Path(data, 'processed')


df = pd.read_csv(Path(data, 'messier_ngc.csv'))
# Obtain hours and minutes of Right Ascension
df['ra_h'] = df['ra'].str.split("h ").str.get(0).astype(int)
df['ra_min'] = df['ra'].str.split("h ").str.get(1).str.replace("m", "").astype(float)
df['ra_original'] = df['ra'].copy()  # Keeps original info
df['ra'] = df['ra_h'] + df['ra_min']/60  # Obtain RA in decimal hours

df['dec_sign'] = df['dec'].str.get(0)
df['dec_degrees'] = np.abs(df['dec'].str.split("d").str.get(0).astype(int))
df['dec_seconds'] = df['dec'].str.split("d ").str.get(1).str.replace("'", "").astype(float)
df['dec_original'] = df['dec'].copy()
df['dec'] = df['dec_degrees'] + df['dec_seconds']/60  # Obtain declination in decimals
df['dec'] = df['dec_sign'] + df['dec'].astype(str)
df['dec'] = df['dec'].astype(float)
df.drop(['ra_h', 'ra_min', 'dec_sign', 'dec_degrees', 'dec_seconds'], axis=1, inplace=True)
# Keeps only originals and in decimals

logger.info(df['type'].unique())
unicodes = {'open cluster': u"\u16b8", 'globular cluster': u"\u2724",
            'emission nebula': u"\u16e5", "star cloud": u"\u2388", "spiral galaxy": u"\u214f", 
            "planetary nebula": u"\u16bb", 'emission nebula, open cluster': u"\u25c8"}
'''
open cluster					Runic Letter Gar			ᚸ
globular cluster					Heavy Four Balloon-Spoked Asterisk			✤
emission nebula					Runic Letter Stan			ᛥ
star cloud					Helm Symbol			⎈
spiral galaxy					Symbol for Samaritan Source			⅏
planetary nebula					Runic Letter Haegl H			ᚻ
emission nebula, open cluster					White Diamond Containing Black Small Diamond			◈
'''
df['code'] = df['type'].replace(unicodes)
df['name_2'] = df['proper_name'].fillna(df['name'])  # If proper name is not given, refer to name
df.to_csv(Path(processed, 'messier_ngc_processed.csv'), index=False)
logger.info(df.head())
