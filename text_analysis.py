import spacy
import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from nltk.tokenize import MWETokenizer
from collections import Counter, defaultdict

nlp = spacy.load('en_core_web_sm')
ps = PorterStemmer()

punctuation_list = ["%","","$","&","£","\\","#","|","!",".",",", "[", "]", "(", ")",":",";","©", "`","``", "”", "\'", "\"","\{", "\}","="]


with open("./dict_companies_pages.json", 'r+') as myfile:
    data=myfile.read()
dict_companies_pages = json.loads(data)


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def is_escaped_unicode(str):
    #how do I determine if this is escaped unicode?
    if is_ascii(str): # escaped unicode is ascii
        return True
    return False


#this function parses the text and retrieves common NE that should be tokenized together
def retrieve_multi_word_tokens_list(list_summaries):
    relevant_words = []
    discard_ne = ["CARDINAL", "ORDINAL", "MONEY", "DATE", "PERCENT", "TIME", "QUANTITY"]

    for document in nlp.pipe(list_summaries, disable=["tagger", "parser"]):
        for element in document.ents:
            #i just remove entities that deal with numbers because are useless
            if element.label_ not in discard_ne:
                relevant_words.append(element)

    return relevant_words

def multi_word_tokenizer(relevant_words, text):
    mwetokenizer = MWETokenizer()

    #add tuples of words into multiword tokenizer
    for word in relevant_words:
        token = str(word).split()
        move_data=[]
        for element in token:
            move_data.append(element)
        tup = tuple(move_data)
        mwetokenizer.add_mwe(tup)

    #execute multitokenization
    return mwetokenizer.tokenize(text)


def analyze_companies_dict(dict_companies_pages):
    list_summaries = list(dict_companies_pages.values())

    relevant_words = retrieve_multi_word_tokens_list(list_summaries)

    for company in dict_companies_pages:
        summary = dict_companies_pages[company]
        
        document = word_tokenize(summary)
        document = multi_word_tokenizer(relevant_words, document)

        print(document)





        






analyze_companies_dict(dict_companies_pages)