import pandas as pd
import numpy as np
import glob
#iterate over files
content = []
files = glob.glob('zillow_files/apartments_scraped_*')
for file in files:
    initial_load = pd.read_csv(file, index_col=0)
    content.append(initial_load)

df = pd.concat(content)

#convert date column from object to datetime
df['Date_Webscraped'] = df['Date_Webscraped'].astype('datetime64')

