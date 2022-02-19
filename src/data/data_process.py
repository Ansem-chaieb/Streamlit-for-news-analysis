import pandas as pd
import numpy as np

import string
import inflect

import spacy
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


wordnet_lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'say', "said", "would", "also"])

sp = spacy.load('en_core_web_sm')
p = inflect.engine()


def data_preprocess(data_path):
    df = pd.read_csv(data_path, index_col=0)
    df['subject'] = np.nan
    for i in range(df.shape[0]):
        parag = list(df['text'][i].split(", "))
        df['subject'][i] = parag[0][2:]

    df['text'] = df['text'].apply(lambda x: text_process(x))

    df['lemma_text'] = df['text'].apply(lambda x: text_process(x, lemmetization=True))
    df['keyword_text'] = df['text'].apply(lambda x: text_process(x, word_cloud=True))
    df['text_ner_names'] = df['text'].apply(lambda x: name_entity_recognition(x, obj = 'name'))
    df['text_ner_count'] = df['text'].apply(lambda x: name_entity_recognition(x, obj='count'))

    df['lemma_subject'] = df['subject'].apply(lambda x: text_process(x, lemmetization=True))
    df['keyword_subject'] = df['subject'].apply(lambda x: text_process(x, word_cloud= True))
    df['subject_ner_names'] = df['subject'].apply(lambda x: name_entity_recognition(x, obj='name'))
    df['subject_ner_count'] = df['subject'].apply(lambda x: name_entity_recognition(x, obj='count'))

    return df


def name_entity_recognition(text, obj=None):
    try:
        sen = sp(text)
    except:
        pass
    l_e = []
    for entity in sen.ents:
        l_e.append(entity.label_)
    e_count = {}
    for e in l_e:
        e_count[e] = l_e.count(e)
    if obj == 'name':
        return list(e_count.keys())
    else:
        return list(e_count.values())
    return


def text_process(text, word_cloud=False, stemming=False, lemmetization=False):
    if lemmetization:
        text = "".join([i for i in text if i not in string.punctuation])
        text = text.lower()
        list_text = (list(text.split(' ')))
        text = [i for i in list_text if i not in stop_words]
        lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
        return lemm_text
    if word_cloud:
        text = "".join([i for i in text if i not in string.punctuation])
        text = text.lower()
        return [c.replace("'", "") for c in text.split(' ') if c not in stop_words]
    # text = convert_number(text)
    parag = ""
    for text in text.split(', ')[1:]:
        if text[-1] == "'" or text[-1] == '"':
            parag += ' ' + text[:-1]
        if text[0] == "'" or text[0] == '"':
            if text[-1] == "'" or text[-1] == '"':
                parag += ' ' + text[1:-1]
            else:
                parag += ' ' + text[1:]
    return parag[1:]


def convert_number(text):
    temp_str = text.split()
    new_string = []
    for word in temp_str:
        if word.isdigit():
            temp = p.number_to_words(word)
            new_string.append(temp)

        else:
            new_string.append(word)
    temp_str = ' '.join(new_string)
    return temp_str
