import numpy as np
import pandas as pd

import spacy
from spacy import displacy
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import streamlit as st
from typing import List, Sequence, Optional, Dict, Union

nlp = spacy.load('en_core_web_sm')
NER_ATTRS = ["text", "label_", "start", "end", "start_char", "end_char"]
TOKEN_ATTRS = ["idx", "text", "lemma_", "pos_", "tag_", "dep_", "head", "morph",
               "ent_type_", "ent_iob_", "shape_", "is_alpha", "is_ascii",
               "is_digit", "is_punct", "like_num", "is_sent_start"]


def result_to_df(result):
    result_dict = {'polarity': result.polarity, "subjectivity": result.subjectivity}
    return pd.DataFrame(result_dict.items(), columns=['metric', 'value'])


def analyze_token_sentiment(docx):
    analyzer = SentimentIntensityAnalyzer()
    pos, neg = {}, {}
    for i in docx.split():
        res = analyzer.polarity_scores(i)['compound']
        if res > 0.1:
            pos[i] = res
        elif res < -0.1:
            neg[i] = res
        else:
            pass
    data_pos = pd.DataFrame({"words": list(pos.keys()), "polarity": list(pos.values())})
    data_neg = pd.DataFrame({"words": list(neg.keys()), "polarity": list(neg.values())})
    return data_pos, data_neg


def data_process(df):
    df['year'] = np.nan
    df['day'] = np.nan
    df['month'] = np.nan
    df['sub_date'] = np.nan
    df['author_name'] = np.nan
    for i in range(df.shape[0]):
        try:
            df['sub_date'].iloc[i] = pd.to_datetime(df['date'].iloc[i][:10])
            df['year'].iloc[i] = int(df['date'].iloc[i][:4])
            df['day'].iloc[i] = int(df['date'].iloc[i][8:10])
            df['month'].iloc[i] = int(df['date'].iloc[i][5:7])
            df['author_name'].iloc[i] = df['author'].iloc[i].replace("By ", "")
        except:
            pass
    return df


def feature_extraction(df):
    lt = list(set(df['author_name']))
    my_list = []
    count = []
    for i in range(len(lt)):
        if len(str(lt[i])) != 3:
            my_list.append(lt[i])
    for i in my_list:
        count.append(df[df['author_name'] == i].shape[0])
    data = {'Author': my_list, "Article_count": count}
    author = pd.DataFrame(data)
    return author


def get_top_n_words(corpus, n=None):
    vec = CountVectorizer(stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


def get_top_n_bigram(corpus, ngram_range, n=None):
    vec = CountVectorizer(ngram_range=(ngram_range, ngram_range)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


def get_list_ner(df):
    text_ner = []
    text_ner_count = []

    for i in range(df.shape[0]):
        text_ner.append(list(df['text_ner_names'].iloc[i][1:-1].replace("'", "").split(', ')))

        text_c = list(df['text_ner_count'].iloc[i][1:-1].replace("'", "").split(', '))
        if text_c[0] == "":
            text_ner_count.append([0])
        else:
            text_ner_count.append([int(i) for i in text_c])

    return text_ner, text_ner_count


def find(c, text_ner, text_ner_count):
    for i, l in enumerate(text_ner):
        try:
            j = l.index(c)
            k = text_ner_count[i][j]
        except ValueError:
            continue
        yield [i, j, k]


def subject_analysis(df):
    df['polarity'] = np.nan
    for i in range(df.shape[0]):
        try:
            parag = df['subject'][i]
            blob = TextBlob(parag)
            result = blob.sentiment.polarity
            df['polarity'].iloc[i] = result
        except:
            pass

    def sentiment(x):
        if x < 0:
            return 'Negative'
        elif x == 0:
            return 'Neutral'
        else:
            return 'Positive'

    try:
        df['sentiment'] = df['polarity'].map(lambda x: sentiment(x))
    except:
        pass
    return df


# this part of  code was taken from spacy streamlit with some modifications


def get_html(html: str):
    """Convert HTML so it can be rendered."""
    WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; 
    margin-bottom: 2.5rem">{}</div> """
    # Newlines seem to mess with the rendering
    html = html.replace("\n", " ")

    return WRAPPER.format(html)


def custom_visualize_ner(
        doc: Union[spacy.tokens.Doc, List[Dict[str, str]]],
        *,
        labels: Sequence[str] = tuple(),
        title: Optional[str] = "Named Entities",
        colors: Dict[str, str] = {},
        manual: Optional[bool] = False,
) -> None:
    if title:
        st.markdown(labels[0])
    html = displacy.render(
        doc,
        style="ent",
        options={"ents": labels, "colors": colors},
        manual=manual,
    )

    style = "<style>mark.entity { display: inline-block }</style>"
    st.components.v1.html(f"{style}{get_html(html)}", width=1400, height=500, scrolling=True)


def visualize_ner(
        doc: Union[spacy.tokens.Doc, List[Dict[str, str]]],
        *,
        labels: Sequence[str] = tuple(),
        attrs: List[str] = NER_ATTRS,
        show_table: bool = True,
        title: Optional[str] = "Named Entities",
        colors: Dict[str, str] = {},
        key: Optional[str] = None,
        manual: Optional[bool] = False,
) -> None:
    """Visualizer for named entities."""
    if title:
        st.header(title)

    if manual:
        if show_table:
            st.warning(
                "When the parameter 'manual' is set to True, the parameter 'show_table' must be set to False."
            )
        if not isinstance(doc, list):
            st.warning(
                "When the parameter 'manual' is set to True, the parameter 'doc' must be of type 'list', "
                "not 'spacy.tokens.Doc'. "
            )
    else:
        labels = labels or [ent.label_ for ent in doc.ents]

    if not labels:
        st.warning("The parameter 'labels' should not be empty or None.")
    else:
        exp = st.expander("Select entity labels")
        label_select = exp.multiselect(
            "Entity labels",
            options=labels,
            default=list(labels),
            key=f"{key}_ner_label_select",
        )
        html = displacy.render(
            doc,
            style="ent",
            options={"ents": label_select, "colors": colors},
            manual=manual,
        )
        style = "<style>mark.entity { display: inline-block }</style>"
        st.components.v1.html(f"{style}{get_html(html)}", width=1400, height=500, scrolling=True)


def display_text(df, list_ner, text_ner, text_ner_count):
    for ner in list_ner:
        ind = sorted([match for match in find(ner,
                                              text_ner=text_ner, text_ner_count=text_ner_count)],
                     key=lambda x: x[2], reverse=True)[0]
        sen = nlp(df['text'].iloc[ind[0]])
        custom_visualize_ner(sen, labels=[ner])
