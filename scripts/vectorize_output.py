import math
import tqdm
import pandas as pd
import numpy as np

from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()

data = pd.read_csv('../Data/AllData - AllData.csv')
data = data.drop([ele for ele in data.columns.to_list()
                 if ele in ['X', 'Random Sort', 'Unnamed: 0']], axis=1)
data = data.dropna(subset=['Description'])
data = data[data.Description != 'For general operating support']
data = data[data.Description != 'For General Operating Support']
data = data[data.Description != 'For operating support']
data = data[data.Description != 'Charitable']
data = data[data.Description != "For the organization's charitable use"]
data = data[data.Description != 'For capital support']
data = data[data.Description != 'For annual support']
data = data[data.Description != 'For annual giving']
data = data[data.Description != 'For general support']
data = data[data.Description != 'OPERATING']
data = data[data.Description != 'For operating support']
data = data[data.Description != 'Operating']
data = data[data.Description != 'OPERATIONAL SUPPORT']
data = data[data.Description != 'Operational support']
data = data[data.Description != 'General Operating Support']
data = data[data.Description != 'General purposes']
data = data[data.Description != 'General purpose']
data = data[data.Description != 'General']
data = data[data.Description != 'Support']
data = data[data.Description.str.lower() != 'general support']
data = data[data.Description.str.lower() != 'for general support']
data = data[data.Description.str.lower() != 'general operating']
data = data[data.Description.str.lower() != 'for general operating']
data = data[data.Description.str.lower() != 'for capital']
data = data[data.Description.str.lower() != 'general operating support']
data = data[data.Description.str.lower() != 'for program support']
data = data.reset_index(drop=True)

data_class = pd.read_csv('../Data/Output/master_output_v2.csv')
data_class = data_class.fillna('-')

pbar = tqdm.tqdm(total=61961)
for idx in range(61961):
    for col in data_class.columns[1:]:
        if type(data_class[col][idx]) == str:
            data_class[col][idx] = data_class[col][idx].split('|')
    pbar.update(1)
pbar.close()

df_final = pd.concat([data, data_class[[' Keywords', ' Categories', 'Locations', 'Bio_Keywords', 'Bioregions']]], axis=1)

df_final = df_final.join(pd.DataFrame(mlb.fit_transform(df_final.pop(' Categories')),columns=['cat_' + x for x in mlb.classes_],index=df_final.index))
df_final = df_final.join(pd.DataFrame(mlb.fit_transform(df_final.pop('Locations')),columns=['loc_' + x for x in mlb.classes_],index=df_final.index))
df_final = df_final.join(pd.DataFrame(mlb.fit_transform(df_final.pop('Bio_Keywords')),columns=['bio_key_' + x for x in mlb.classes_],index=df_final.index))
df_final = df_final.join(pd.DataFrame(mlb.fit_transform(df_final.pop('Bioregions')),columns=['bio_reg_' + x for x in mlb.classes_],index=df_final.index))

df_final = df_final.drop(['cat_-', 'loc_-', 'bio_key_', 'bio_reg_'])
df_final.to_csv('../Data/Output/master_output_data_analysis_v1.csv', index=False)
