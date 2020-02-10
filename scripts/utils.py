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

    for phrase in preproc_phrase:
        data = data[data.Description.str.lower() != phrase]

    data_sentences = data.Description.values.tolist()
    data_sentences = [x.lower() for x in data_sentences]

    return data_sentences


def extract_keywords_from_csv(file):
    keywords_df = pd.read_csv(file)
    keywords_df = keywords_df.drop(['Unnamed: 31', 'Unnamed: 32'], axis=1)
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

    stopwords_cats = [x.strip() for x in list(stopwords_df)]
    stopwords = []
    for idx in range(len(stopwords_cats)):
        stopwords.append(list(set(stopwords_df[stopwords_cats[idx]].dropna())))
    stopwords = [x.lower() for x in stopwords]

    pbar = tqdm.tqdm(total=len(output_data))
    for idx in range(len(output_data)):
        class_cats = output_data.iloc[idx]['Categories'].split('|')
        for stop_idx, stop_cat in enumerate(stopwords_cats):
            if stop_cat in class_cats:
                for stopword in stopwords[stop_idx]:
                    if string_found(stopword,
                                    output_data.iloc[idx]['Description'].lower()):
                        class_cats.remove(stopword)
        output_data.iloc[idx]['Categories'] = '|'.join(class_cats)
        pbar.update(1)
    pbar.close()

    return output_data
