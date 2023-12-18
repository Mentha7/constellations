import pandas as pd
import numpy as np

# Load dataframe directly from gzip file
# Set low_memory=False to ensure no mixed types
df = pd.read_csv('data/hygdata_v37.csv.gz', compression='gzip', header=0, sep=',', quotechar='"', low_memory=False)
print(df.head())

# Check all column names
print(df.columns.values)

'''
Fields in the HYG (Hipparcos-Yale-Gliese) Database
1. StarID: The database primary key from a larger "master database" of stars.
2. HD: The star's ID in the Henry Draper catalog, if known.
3. HR: The star's ID in the Harvard Revised catalog, which is the same as its number in the Yale Bright Star Catalog.
4. Gliese: The star's ID in the third edition of the Gliese Catalog of Nearby Stars.
5. BayerFlamsteed: The Bayer / Flamsteed designation, from the Fifth Edition of the Yale Bright Star Catalog. This is a combination of the two designations. The Flamsteed number, if present, is given first; then a three-letter abbreviation for the Bayer Greek letter; the Bayer superscript number, if present; and finally, the three-letter constellation abbreviation. Thus Alpha Andromedae has the field value "21Alp And", and Kappa1 Sculptoris (no Flamsteed number) has "Kap1Scl".
6. RA, Dec: The star's right ascension and declination, for epoch 2000.0. Stars present only in the Gliese Catalog, which uses 1950.0 coordinates, have had these coordinates precessed to 2000.
7. ProperName: A common name for the star, such as "Barnard's Star" or "Sirius". I have taken these names primarily from the Hipparcos project's web site, which lists representative names for the 150 brightest stars and many of the 150 closest stars. I have added a few names to this list. Most of the additions are designations from catalogs mostly now forgotten (e.g., Lalande, Groombridge, and Gould ["G."]) except for certain nearby stars which are still best known by these designations.
8. Distance: The star's distance in parsecs, the most common unit in astrometry. To convert parsecs to light years, multiply by 3.262. A value of 10000000 indicates missing or dubious (e.g., negative) parallax data in Hipparcos.
9. Mag: The star's apparent visual magnitude.
10. AbsMag: The star's absolute visual magnitude (its apparent magnitude from a distance of 10 parsecs).
11. Spectrum: The star's spectral type, if known.
12. ColorIndex: The star's color index (blue magnitude - visual magnitude), where known.
13. * X,Y,Z: The Cartesian coordinates of the star, in a system based on the equatorial coordinates as seen from Earth. +X is in the direction of the vernal equinox (at epoch 2000), +Z towards the north celestial pole, and +Y in the direction of R.A. 6 hours, declination 0 degrees.
14. * VX,VY,VZ: The Cartesian velocity components of the star, in the same coordinate system described immediately above. They are determined from the proper motion and the radial velocity (when known). The velocity unit is parsecs per year; these are small values (around 10-5 to 10-6), but they enormously simplify calculations using parsecs as base units for celestial mapping.
'''

# Remove the Sun...
df = df[df['proper'] != 'Sol']

# Plaintext Bayer designations to unicode greek letters
greek = {'Alp': u"α",'Bet': u"β",'Chi': u"χ",'Del': u"δ",'Eps': u"ε",'Eta': u"η",
         'Gam': u"γ",'Iot': u"ι",'Kap': u"κ",'Lam': u"λ",'Mu': u"μ",'Nu': u"ν",
         'Ome': u"ω",'Omi': u"ο",'Phi': u"φ",'Pi': u"π",'Psi': u"ψ",'Rho': u"ρ",
         'Sig': u"σ",'Tau': u"τ",'The': u"θ",'Ups': u"υ",'Xi': u"ξ",'Zet': u"ζ"}

print(df.bayer.dropna().unique())       # df['bayer'] is an ndarray while df.bayer is an array
print(len(df.bayer.dropna().unique()))  # 103 unique Bayer designations

def unicode_greek(n):
    if str(n) == 'nan':
        return np.nan
    split = n.split('-')
    split[0] = greek.get(split[0])
    return ''.join(split)

df['unicode_greek'] = df['bayer'].apply(unicode_greek)
print(df.unicode_greek.unique())

print(len(df.spect.dropna().unique()))

'''
Morgan-Keenan designations (The MK system) uses O, B, A, F, G, K and M for designation of the hot (O) to cool (M).
'''
def get_first_letter(name):
    '''Preprocess spectral designations.
    '''
    if str(name)[0:2] == 'sd':
        name = name[2::]
        get_first_letter(name)
    if str(name)[0].isupper() and str(name)[0] != 'D':
        return name[0]
    else:
        # print(str(name)[0:2])  # For debugging
        return np.nan


df['dist'].replace(to_replace=100000, value=np.nan, inplace=True)  # Remove bad value

df['spect_desig'] = df['spect'].apply(get_first_letter)

print(df.spect_desig.dropna().unique())
print(len(df.spect_desig.dropna().unique()))
# ['F' 'K' 'B' 'G' 'M' 'A' 'C' 'R' 'O' 'W' 'N' 'S']


color_dict = {
    'O':'#5A90C3', 'B':'#93C2F1', 'A':'#f3e8d3', 'F':'#d4bf94',
    'G':'#FFD423', 'K':'#F99220', 'M':'#FF2620',  'C':'#979330',
    'R':'#979330', 'W':'#979330', 'N':'#979330', 'S':'#979330',
    np.nan : '#000000' # unknown
}

df['color'] = df['spect_desig'].replace(to_replace=color_dict)
df['linecolor'] = df['color'].replace(['#000000'], ['#f3e8d3'])  # Beige outline for black NANs

print(df.head(20))

df.to_csv('data/processed/hygdata_v37_processed.csv', index=False)


print('----Stats HYG Database----')
print(len(df), 'total stars available in the database.')
df = df[df['mag'] <= 6.5]
print(len(df), 'stars visible to the human eye.')
df.to_csv('data/processed/hygdata_v37_mag65.csv', index=False)
