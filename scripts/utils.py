import re
import csv
import tqdm
import numpy as np
import pandas as pd


def string_found(string1, string2):
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False


def preprocess_data(raw_data, preprocess_phrases):
    data = pd.read_csv(raw_data)
    preproc_ph = pd.read_csv(preprocess_phrases)
    preproc_phrases = list(preproc_ph.Phrases)
    data = data.drop([ele for ele in data.columns.to_list()
                      if ele not in ['Description']], axis=1)
    data = data.dropna().reset_index(drop=True)

    for phrase in preproc_phrases:
        data = data[data.Description.str.lower() != phrase]

    data_sentences = data.Description.values.tolist()
    data_sentences = [x.lower() for x in data_sentences]

    return data_sentences


def extract_keywords_from_csv(file):
    keywords_df = pd.read_csv(file)
    category_names = [x.strip() for x in list(keywords_df)]
    keywords = []

    for idx in range(len(category_names)):
        keywords.append(list(set(keywords_df[category_names[idx]].dropna())))

    return category_names, keywords


def categorize_grants(data_sentences, category_names, keywords):
    grant_categories = []
    grant_keywords = []

    pbar = tqdm.tqdm(total=len(data_sentences))
    for grant in data_sentences:
        curr_cat = []
        curr_key = []
        for idx in range(len(category_names)):
            for keyword in keywords[idx]:
                if string_found(keyword, grant):
                    curr_key.append(keyword.replace(' ', '_'))
                    curr_cat.append(category_names[idx])
        curr_key = list(set(curr_key))
        curr_cat = list(set(curr_cat))
        grant_categories.append(curr_cat)
        grant_keywords.append(curr_key)
        pbar.update(1)
    pbar.close()

    return grant_categories, grant_keywords


def get_output_grants(data_sentences, grant_keywords, grant_categories):
    output_grants = []

    pbar = tqdm.tqdm(total=len(data_sentences))
    for idx in range(len(data_sentences)):
        temp = []
        temp.append(data_sentences[idx])
        temp.append("|".join(grant_keywords[idx]))
        temp.append("|".join(grant_categories[idx]))
        output_grants.append(temp)
        pbar.update(1)
    pbar.close()

    return output_grants


def apply_stopwords(output_grants, stopwords_csv):
    output_data = pd.read_csv(output_grants)
    stopwords_df = pd.read_csv(stopwords_csv)
    
    output_data['Stopwords'] = "-"
    output_data['Filtered_Categories'] = "-"

    stopwords_dict = dict()
    for cat in [x.strip() for x in list(stopwords_df)]:
        temp = list(set(stopwords_df[cat].dropna()))
        temp = [x.lower() for x in temp]
        stopwords_dict[cat] = temp

    pbar = tqdm.tqdm(total=len(output_data))
    for idx in range(len(output_data)):
        class_cats = set(output_data.iloc[idx]['Categories'].split('|'))
        stop_added = set()
        flag = False
        
        for stop_cat in stopwords_dict.keys():
            if stop_cat in class_cats:
                for stopword in stopwords_dict[stop_cat]:
                    if string_found(stopword,
                                    output_data.iloc[idx]['Description'].lower()):
                        class_cats.discard(stop_cat)
                        stop_added.add(stopword)
        output_data.loc[idx,'Filtered_Categories'] = '|'.join(list(class_cats))
        if len(stop_added) > 0:
            output_data.loc[idx, 'Stopwords'] = '|'.join(list(stop_added))
        pbar.update(1)
    pbar.close()

    return output_data
