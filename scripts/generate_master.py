import tqdm
import numpy as np
import pandas as pd

from utils import string_found
from utils import preprocess_data
from utils import extract_keywords_from_csv
from utils import categorize_grants
from utils import get_output_grants

'''
Path to data files
'''
keywords_classified = '/home/psd2120/research/Data/Output/output_grants_v12_filtered.csv'
bioregion_classified = '/home/psd2120/research/Data/Output/output_bioregions_v6.csv'
output_file = '/home/psd2120/research/Data/Output/Master Output/v9/master_output_v9_temp.csv'

'''
Merge the classification files
'''
data_class = pd.read_csv(keywords_classified)
data_bio = pd.read_csv(bioregion_classified)
df_master = pd.concat([data_class, data_bio[['Bio_keywords', 'Bio_regions']]], axis=1)
df_master = df_master.fillna('-')
df_master.to_csv(output_file, index=False)
print('Saved master output file.')
