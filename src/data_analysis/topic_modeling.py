import spacy

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel, Phrases, phrases, ldamodel

import pyLDAvis
import pyLDAvis.gensim


class LatentDirichletAllocation:
    def __init__(self, df):
        self.dataset = df
        self.data = self.dataset.text.values.tolist()

        self.en = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        self.stopwords = list(self.en.Defaults.stop_words)
        self.stopwords.extend(['from', 'subject', 're', 'edu', 'use', 'say', "said", "would", "also"])

        self.lemma_data = self.data_process()
        self.id_word = corpora.Dictionary(self.lemma_data)
        self.corpus = self.input_process()

    def remove_stopwords(self, texts):
        return [[word for word in text if word not in self.stopwords] for text in texts]

    def create_bigrams(self, texts, bigram_mod):
        return [bigram_mod[text] for text in texts]

    def lemmatization(self, texts, allowed_posttags=None):
        if allowed_posttags is None:
            allowed_posttags = ['NOUN', 'ADJ', 'VERB', 'ADV']
        out = []
        for text in texts:
            out.append([token.lemma_ for token in self.en(" ".join(text)) if token.pos_ in allowed_posttags])
        return out

    def data_process(self):
        data_words = []
        for parag in self.data:
            data_words.append(simple_preprocess(parag, deacc=True))
        filtered_data_words = self.remove_stopwords(data_words)

        bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
        bigram_mod = gensim.models.phrases.Phraser(bigram)
        bigrams_data_words = self.create_bigrams(filtered_data_words, bigram_mod)

        lemma_data = self.lemmatization(bigrams_data_words)
        return lemma_data

    def input_process(self):
        return [self.id_word.doc2bow(text) for text in self.lemma_data]

    def lda(self):
        self.lda_model = ldamodel.LdaModel(corpus=self.corpus,
                                           id2word=self.id_word,
                                           num_topics=5,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

        perplexity = self.lda_model.log_perplexity(self.corpus)
        coherance_model = CoherenceModel(model=self.lda_model, texts=self.lemma_data, dictionary=self.id_word,
                                         coherence='c_v')
        coherance_lda = coherance_model.get_coherence()

        return perplexity, coherance_lda

    def visualisation(self):
        perplexity, coherance_lda = self.lda()
        vis = pyLDAvis.gensim.prepare(self.lda_model, self.corpus, self.id_word)
        return perplexity, coherance_lda, vis
