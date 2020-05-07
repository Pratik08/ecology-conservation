import re
import csv
import tqdm
import numpy as np
import pandas as pd

from utils import string_found
from utils import apply_stopwords

'''
Path to data files
'''
output_grants = '/home/psd2120/research/Data/Output/output_grants_v12.csv'
stopwords_csv = '/home/psd2120/research/Data/Stopwords/Stopwords_Alphabetized_v5.csv'

proc_output = apply_stopwords(output_grants, stopwords_csv)
proc_output.to_csv(output_grants, index=False)

print('Saved output.')
print('Post-processing completed.')
