import numpy as np
import pandas as pd

from pathlib import Path

from logger import logger

'''
Catalogue of Constellation Boundary Data
    Davenhall A.C., Leggett S.K.
    <Royal Obs. Edinburgh (1989)>

Description:
    A computer readable catalog of constellation boundary data is
    presented in a form suitable for the construction of star charts and
    atlases. Two data files are available, one for equator and equinox
    1875 and the other for equator and equinox 2000. In addition to the
    data files a documentation file is available that includes a table
    listing the abbreviations used for the constellations as well as a
    more detailed discussion of the preparation of the catalog.

    The present catalog of constellation boundary data is complementary to
    that of Roman (1987). Roman's catalog should be used to determine in
    which constellation an object lies in. The present catalog is more
    suited to the construction of star charts and atlases. Both catalogs
    were based on Delporte (1930).

Byte-by-byte Description of file: bound_20.dat
      ______________________________
     | Number of records   |  13422 |
     | Record size (bytes) |    29  |
     |_____________________|________|_
--------------------------------------------------------------------------------
   Bytes  Format   Units   Label   Explanations
--------------------------------------------------------------------------------
   1- 10   F10.7   h       RAhr    Right ascension in decimal hours (J2000)
  12- 22   F11.7   deg     DEdeg   Declination in degrees (J2000)
  24- 27   A4      ---     cst     Constellation abbreviation
      29   A1      ---     type    [OI] Type of point (Original or Interpolated)
--------------------------------------------------------------------------------
'''
processed = Path('data/processed')

colwidths = [11, 11, 5, 100]
colnames = ['right_ascension_hours', 'declination_degrees', 'const_abbreviation', 'type_point']

df = pd.read_fwf('data/bound_20.dat.gz', compression='gzip', widths=colwidths, names=colnames)
logger.info(df.head())


# Group by constellation abbreviation
const, ras, decs = [], [], []

for name, group in df.groupby('const_abbreviation'):
    const.append(name)
    ras.append(group['right_ascension_hours'].tolist())
    decs.append(group['declination_degrees'].tolist())
    
df_ra_dec = pd.DataFrame(data={'name':const, 'ra':ras, 'dec':decs})
logger.info(df_ra_dec.head())

savename = 'constellations.csv'
df_ra_dec.to_csv(Path(processed, savename), index=False)