import wikipedia
import json
import pandas as pd

example_list = ["Apple", "Facebook", "Banca Intesa San Paolo", "Unicredit"]

df = pd.read_csv("./bloomberg_perimeter_1000.csv")

print(list(df))

companies_list = list(df.LONG_COMP_NAME)

print(companies_list)

f = open("./companies_list.json", "w+")
json_data = json.dumps(companies_list)
f.write(json_data)  

##TODO how to disambiguate? depends on the format of the name in the input list.
## risk of not finding a name because of slight string format difference
## risk of disambiguation without raising exception (es looking at Apple returns page of the fruit)

#create dictionary of name-summary of wikipedia page
dict_companies_pages = {}
dict_companies_summaries= {}

def wiki_extractor(companies_list):
    for name in companies_list:
        if name not in dict_companies_pages:

            try:
                page = wikipedia.WikipediaPage(str(name))
                content = page.content
                summary = page.summary
                dict_companies_pages[name] = content
                dict_companies_summaries[name] = summary

            except wikipedia.exceptions.PageError:
                print("pageError")
                #page_error.append(term)
                continue

            except wikipedia.exceptions.DisambiguationError:
                print("disambiguation")
                #page_error.append(term)
                continue 

wiki_extractor(companies_list)

print("rate of found pages: "+str(len(dict_companies_pages)/len(companies_list)))

f = open("./dict_companies_pages.json", "w+")
json_data = json.dumps(dict_companies_pages)
f.write(json_data)  

f = open("./dict_companies_summaries.json", "w+")
json_data = json.dumps(dict_companies_summaries)
f.write(json_data)  