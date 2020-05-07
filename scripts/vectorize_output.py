import math
import tqdm
import pandas as pd
import numpy as np

from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()

'''
Path to data files
'''
raw_data = '/home/psd2120/research/Data/AllData - AllData.csv'
preprocess_phrases = '/home/psd2120/research/Data/Preprocessing/Preprocessing_Phrases_v3.csv'
master_file = '/home/psd2120/research/Data/Output/Master Output/v9/master_output_v9_temp.csv'
output_file = '/home/psd2120/research/Data/Output/Master Output/v9/master_output_data_analysis_v9.csv'

'''
Preprocess
'''
data = pd.read_csv(raw_data)
preproc_ph = pd.read_csv(preprocess_phrases)
preproc_phrases = list(preproc_ph.Phrases)
data = data.drop([ele for ele in data.columns.to_list() if ele in ['X', 'Random Sort', 'Unnamed: 0']], axis=1)
data = data.dropna(subset=['Description'])

for phrase in preproc_phrases:
    data = data[data.Description.str.lower() != phrase]

data = data.reset_index(drop=True)

data_class = pd.read_csv(master_file)
data_class = data_class.fillna('-')

pbar = tqdm.tqdm(total=len(data))
for idx in range(len(data)):
    for col in data_class.columns[1:]:
        if type(data_class[col][idx]) == str:
            data_class[col][idx] = data_class[col][idx].split('|')
    pbar.update(1)
pbar.close()

'''
Generate output file
'''
df_final = pd.concat([data, data_class[['Keywords','Filtered_Categories', 'Bio_keywords','Bio_regions']]], axis=1)
df_final = df_final.join(pd.DataFrame(mlb.fit_transform(df_final.pop('Filtered_Categories')),columns=['cat_' + x for x in mlb.classes_],index=df_final.index))
df_final = df_final.join(pd.DataFrame(mlb.fit_transform(df_final.pop('Bio_keywords')),columns=['bio_key_' + x for x in mlb.classes_],index=df_final.index))
df_final = df_final.join(pd.DataFrame(mlb.fit_transform(df_final.pop('Bio_regions')),columns=['bio_reg_' + x for x in mlb.classes_],index=df_final.index))
df_final = df_final.drop(['cat_-', 'bio_key_-', 'bio_reg_-'], axis=1)
df_final.to_csv(output_file, index=False)

print('Completed')
