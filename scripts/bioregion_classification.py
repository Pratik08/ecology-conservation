import re
import csv
import tqdm
import numpy as np
import pandas as pd

from utils import string_found
from utils import preprocess_data
from utils import categorize_grants
from utils import get_output_grants

'''
Path to data files
'''
raw_data = '../Data/AllData - AllData.csv'
bioregion_keywords = '../Data/Biogeographic_Realms_Ecoregions.csv'
preprocess_phrases = '../Data/Preprocessing_Phrases.csv'
output_file = '../Data/Output/output_bioregions_v3.csv'

'''
Preprocessing to remove grants which are empty, operating support,
program support, etc.
'''
data_sentences = preprocess_data(raw_data, preprocess_phrases)
print('Preprocessed data.')

'''
Extract keywords from CSV
'''
df_eco = pd.read_csv(bioregion_keywords)
category_names = list(df_eco)
keywords = []
for idx in range(len(category_names)):
    temp = list(set(df_eco[category_names[idx]].dropna()))
    temp = [x.lower() for x in temp]
    keywords.append(temp)

'''
Categorize Grants
'''
grant_categories, grant_keywords = categorize_grants(data_sentences,
                                                     category_names, keywords)
print('Categorized grants.')

'''
Store description, keywords and categories as csv
'''
output_grants = get_output_grants(data_sentences, grant_keywords,
                                  grant_categories)

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output_grants)

print('Saved output.')
print('Classification completed.')
