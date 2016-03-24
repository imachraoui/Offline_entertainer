import json
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource
import datetime
from datetime import date
from datetime import timedelta
import calendar
import urllib3
from collections import Counter
import operator
import nltk
from nltk.probability import *
from nltk.corpus import *
from nltk import word_tokenize
from nltk import *
import itertools
import numpy as np
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer

class TextLearning() :

    reg_words = r"(?x)"
    # Smileys
    reg_words += "(?:[:=;] [oO\-]? [D\)\]\(\]/\\OpP])"
    # nombres
    reg_words += "| (?:(?:\d+,?)+(?:\.?\d+)?)"
    reg_words += "| (\$|\€)?\d+(\.\d+)?%?"
    # contractions d', l', ...
    reg_words += "| \w'"
    reg_words += "| \w+"
    reg_words = r"\w'"
    reg_words += '|((?<=[^\w\s])\w(?=[^\w\s])|(\W))+'
    stop_words_location = 'C:/Users/wymeka/Documents/ENSAE/Projet-Python/Offline-entertainer/org/ensae/offline_entertainer/server/learning/rss'

    frenchStemmer=nltk.stem.SnowballStemmer('french', ignore_stopwords=True)
    englishStemmer=nltk.stem.SnowballStemmer('english', ignore_stopwords=True)
    frenchWordTokenizer=RegexpTokenizer(reg_words,gaps=True)

    recommendation_model = None
    text_vectorizer = None

    def __init__(self,language) :
        if(language == 'english'):
            self.stemmer = self.englishStemmer
            self.word_tokenizer = self.frenchWordTokenizer
            self.stop_words = self.load_stopwords(language)
        else :
            self.stemmer = self.frenchStemmer
            self.word_tokenizer = self.frenchWordTokenizer
            self.stop_words = self.load_stopwords('french')

    @staticmethod
    def get_weighted_domains(articles):

        domains_indexed = {}
        domains = []
        for article in articles :
            domain= urllib3.util.parse_url(article["url"]).host
            domains.append(domain)
            if(domains_indexed.get(domain) == None):
                domains_indexed[domain]=[]

            domains_indexed[domain].append(int(article["time_added"]))

        times_added = list(domains_indexed.values())
        maxvalues = lambda x : (x,max(domains_indexed[x]))
        recent_articles = list(map(maxvalues,domains_indexed))

        # from most recent to less recent
        ordered_recent_articles = sorted(recent_articles, key=operator.itemgetter(1),reverse=True)

        # Computation of a window of articles selection in the last 30 days starting from the last added article
        time_last_article = ordered_recent_articles[0][1]
        date_last_added_article = date.fromtimestamp(time_last_article)
        window_selection_articles = date_last_added_article - timedelta(days=30)
        window_selection_articles_timestamp = calendar.timegm(window_selection_articles.timetuple())

        # sort domains by frequency
        frequency = sorted(Counter(domains).items(), key=operator.itemgetter(1),reverse=True)
        meanFrequency = np.mean(list(Counter(domains).values()))

        favourite_sites={}
        i=2
        for recent in ordered_recent_articles :
            favourite_sites[recent[0]]=i
            i = i - 1
            if (favourite_sites[recent[0]] > window_selection_articles_timestamp )|(i <=0):
                break
        j=10
        for one in frequency :
            if favourite_sites.get(one[0]) == None :
                favourite_sites[one[0]] = 0
            favourite_sites[one[0]]= favourite_sites[one[0]] + j
            j = j- 2
            if (favourite_sites[one[0]] < meanFrequency) | (j <= 0):
                break
        return(sorted(favourite_sites.items(), key=operator.itemgetter(1),reverse=True))

    def getwordsfromarticle(self,articles_for_user):
        words =[]
        for article in articles_for_user :
            words.append(word_tokenize(article["text"]))
        words = itertools.chain(*words)
        return(list(words))

    @staticmethod
    def detect_language(words_text):
        files = stopwords.fileids()
        inter_length = np.zeros_like(files,dtype=np.int64)
        test={}
        i=0
        for file in files :
            inter_length[i] = len(set(words_text).intersection(stopwords.words(file)))
            test[file]=len(set(words_text).intersection(stopwords.words(file)))
            i +=1
        return(files[np.argmax(inter_length)])

    def load_stopwords(self,language):
        split = lambda x : x.rsplit()
        if language == 'french':
            with open(self.stop_words_location+'/stopwords-fr.txt', 'r',encoding="utf-8") as f:
                stopwords = map(split,f.readlines())
        else:
           with open(self.stop_words_location+'/stopwords-en.txt', 'r',encoding="utf-8") as f:
                stopwords = map(split,f.readlines())
        stopwords = itertools.chain(*stopwords)
        return(list(stopwords))

    def get_stemmed_texts(self,userid,file_path,with_category):
        with open(file_path, 'r') as f:
            articles = json.load(f)
            o = json.dumps(articles[userid])
            articles_for_user = json.loads(o)
            texts = []
            for id in articles_for_user :
                text=articles_for_user[id]["title"]+ " "+articles_for_user[id]["text"]
                stemmed_words = self.stem(word_tokenize(text))
                text = ' '.join(stemmed_words)
                if with_category:
                    texts.append((text,articles_for_user[id]['category']))
                else:
                    texts.append(text)
        return(texts)

    def remove_stopwords(self,words):

        words_rmg =[]
        lower_lambda =  lambda x : x.lower()
        tokens = [self.word_tokenizer.tokenize(s) for s in words]
        for word in map(lower_lambda,list(itertools.chain(*tokens))):
            if (word.lower() not in self.stop_words) & (len(word) > 3):
                words_rmg.append(word)

        return(words_rmg)

    def stem(self,words):
        stemmed_words = [str(self.stemmer.stem(w)) for w in words]
        return(stemmed_words)

    @staticmethod
    def get_areas_of_interest(user_id) :
        tuple_texts_test = TextLearning('english').get_stemmed_texts(user_id,'../data/pocket/pocket_formatted_data.json',False)
        test_matrix_real= TextLearning.text_vectorizer.transform(tuple_texts_test)
        categories_real = TextLearning.recommendation_model.predict(test_matrix_real)
        return(sorted(Counter(categories_real).items(), key=operator.itemgetter(1),reverse=True))


