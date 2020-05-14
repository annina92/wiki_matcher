import spacy
import json
import re
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from nltk.tokenize import MWETokenizer
from nltk.corpus import words, stopwords, wordnet

from collections import Counter, defaultdict


#######################################################
#       UTILITIES
#######################################################

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

number_patterns = r"[0-9].*"

def dummy(doc):
    return doc

def create_vectorizer(ngrams):
    vectorizer = TfidfVectorizer(
        analyzer='word',
        tokenizer=dummy,
        preprocessor=dummy,
        token_pattern=None,
        use_idf=True,
        ngram_range=(ngrams,ngrams),
        sublinear_tf =True)  

    return vectorizer

########################################################


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


#function takes as input the dictionary of company-summary and the number of keywords to retrieve
def analyze_data(dict_companies_pages, n):
    list_summaries = list(dict_companies_pages.values())
    #list to be fed to tfidf vectorizer
    tfidf_list = []
    #dict to keep track of companies and their text
    dict_index_company_name = {}

    #dict for storing name of company-keyword list
    dict_company_keylist = {}

    relevant_words = retrieve_multi_word_tokens_list(list_summaries)
    counter =0
    for company in dict_companies_pages:
        summary = dict_companies_pages[company]
        
        document = word_tokenize(summary)
        document = multi_word_tokenizer(relevant_words, document)

        #remove useless punctuation from tokens (es. Apple$ (dirty text happens sometimes)) and numbers
        document = [x.lower().replace("_", " ").replace("|"," ").replace("\\"," ").replace("!"," ").replace("\""," ").replace("£"," ").replace("$"," ").replace("%"," ").replace("&", " ").replace("-"," ").replace("("," ").replace(")"," ").replace("="," ").replace("?"," ").replace("^"," ").replace(","," ").replace("@"," ").replace("#"," ").replace("\'"," ").replace("~", " ").replace("/", " ") for x in document]
        document = [re.sub(number_patterns, "", x) for x in document]

        #final clean of stopwords, empty elements, words shorter than threshold and single punctuation tokens
        #stemming is to decrease number of features, while matching similar words with the same string, so to count correct frequencies.
        document = [ps.stem(x) for x in document if (x is not " ")and (is_escaped_unicode(x)) and (x not in punctuation_list) and (x not in stopwords.words('english')) and (len(x)>1)]

        print(document)
        tfidf_list.append(document)
        dict_index_company_name[counter] = company
        counter+=1

    
    vectorizer = create_vectorizer(1)
    vectorizer.fit(tfidf_list)
    tfidf_vectors = vectorizer.transform(tfidf_list)
    #terms contain the names of all the words that are the features of this model
    terms = vectorizer.get_feature_names()

    #this matrix contain n_docs number of rows and m_terms number of unique terms. Each cell contains a tfidf score for word in a specific document.
    tfidf_matrix = tfidf_vectors.toarray()


    #scan each row = document of the matrix to look n words with highest tfidf score
    for i in range(tfidf_matrix.shape[0]):
        row = tfidf_matrix[i]

        #with this function i can order only part of a vector (for efficiency). Ordered_indices is a list of the indices of the highest values of row
        ordered_indices = np.argpartition(-row,range(n))
        keyword_list = []
        for j in range(n):
            #from term vector, I can get the word corresponding the highest tfidf values
            keyword_list.append(terms[ordered_indices[j]])

        #use dict index company name to retrieve name of company based on the index of the matrix
        dict_company_keylist[dict_index_company_name[i]] = keyword_list
        



    return dict_company_keylist

        






print(analyze_data(dict_companies_pages, 6))