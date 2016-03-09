import json
from org.ensae.offline_entertainer.data.pocket.PocketResource import PocketResource
import datetime
import urllib3
from collections import Counter
import operator
import nltk
# from nltk.book import *
from nltk.probability import *
# from nltk.corpus import gutenberg
from nltk.corpus import *
from nltk import word_tokenize
from nltk import *
import itertools
import numpy as np
from nltk.tokenize import RegexpTokenizer
#from org.ensae.offline_entertainer.data.pocket import articles_service
import org.ensae.offline_entertainer.server.learning.lib.RSSFeedsHelper as rssfeedsHelper

class TextLearning() :
    def getDomains(userid):
        articles = articles_service.get_articles(userid)
        domains = []
        for article in articles :
            domain= urllib3.util.parse_url(article["url"]).host
            domains.append(domain)

        return(sorted(Counter(domains).items(), key=operator.itemgetter(1),reverse=True))

    def getwordsfromarticle(userid):
        with open('../../data/pocket/pocket_formatted_data.json', 'r') as f:
            articles = json.load(f)
            o = json.dumps(articles[userid])
            articles_for_user = json.loads(o)
            words =[]
            for id in articles_for_user :
                words.append(word_tokenize(articles_for_user[id]["text"]))
            #words = itertools.chain(*words)
        #return(list(words))
        return(words)
    #print(getDomains("1"))
    #gutenberg.sents('text1')
    #print(stopwords.words('french'))
    # a = wordnet.synsets('french')
    # b = wordnet.synset(a[0].name()).hyponyms()[0].lemmas()
    # print(b)
    # c=sorted(lemma.name()for lemma in b)
    # print(c)
    #
    # print(words.words('en')[500:600])

    def texts(userid):
        with open('pocket_formatted_data.json', 'r') as f:
            articles = json.load(f)
            o = json.dumps(articles[userid])
            articles_for_user = json.loads(o)
            texts = []
            for id in articles_for_user :
                texts.append(articles_for_user[id]["text"])
        return(texts)

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

    def remove_stopwords(words):
        reg_words = r"(?x)"
        reg_words += "(?:[:=;] [oO\-]? [D\)\]\(\]/\\OpP])"                                      # Smileys
        reg_words += "| (?:(?:\d+,?)+(?:\.?\d+)?)"                                              # numbers with different variants of format
        reg_words += "| (\$|\€)?\d+(\.\d+)?%?"                                                 # percentages and money EUR and USD - NOT USED HERE
        #reg_words += "| \w'"                                                                    # contractions d', l', ...
        reg_words += "| \w+"                                                                    # plain words
        #reg_words += "| [^\w\s]"                                                                # punctuations
        reg_words = r"\w'"
        reg_words += '|((?<=[^\w\s])\w(?=[^\w\s])|(\W))+'

        frenchWordTokenizer=RegexpTokenizer(reg_words,gaps=True)

        words =""
        stopwords_fr = stopwords.words('french')
        stopwords_en = stopwords.words('english')
        words_rmg =[]
        lower_lambda =  lambda x : x.lower()
        for word in map(lower_lambda,words):
            if (word.lower() not in stopwords_fr) & (word.lower() not in stopwords_en):
                words_rmg.append(word)
        tokens = [frenchWordTokenizer.tokenize(s) for s in words_rmg]
        return(list(itertools.chain(*tokens)))

    def stem(words):
        frenchStemmer=nltk.stem.SnowballStemmer('french', ignore_stopwords=True)
        englishStemmer=nltk.stem.SnowballStemmer('english', ignore_stopwords=True)
        return([frenchStemmer.stem(operator.itemgetter(0)(w)) for w in words])


