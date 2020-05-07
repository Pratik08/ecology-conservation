import re
import csv
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
raw_data = '/home/psd2120/research/Data/AllData - AllData.csv'
bioregion_keywords = '/home/psd2120/research/Data/Biogeographic_Realms_Ecoregions.csv'
preprocess_phrases = '/home/psd2120/research/Data/Preprocessing/Preprocessing_Phrases_v3.csv'
output_file = '/home/psd2120/research/Data/Output/output_bioregions_v7.csv'

'''
Preprocessing to remove grants which are empty, operating support,
program support, etc.
'''
data_sentences = preprocess_data(raw_data, preprocess_phrases)
print('Preprocessed data.')

'''
Extract keywords from CSV
'''
category_names, keywords = extract_keywords_from_csv(bioregion_keywords)
print('Extracted keywords.')

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
    writer.writerow(['Description', 'Bio_keywords', 'Bio_regions'])
    writer.writerows(output_grants)

print('Saved output.')
print('Classification completed.')
