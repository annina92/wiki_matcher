import wikipedia
import json

example_list = ["Apple", "Facebook", "Banca Intesa San Paolo", "Unicredit"]


##TODO how to disambiguate? depends on the format of the name in the input list.
## risk of not finding a name because of slight string format difference
## risk of disambiguation without raising exception (es looking at Apple returns page of the fruit)

#create dictionary of name-summary of wikipedia page
dict_companies_pages = {}

def wiki_extractor(companies_list):
    for name in companies_list:
        if name not in dict_companies_pages:

            try:
                page = wikipedia.WikipediaPage(str(name)).summary
                print(page)
                dict_companies_pages[name] = page
            except wikipedia.exceptions.PageError:
                print("pageError")
                #page_error.append(term)
                continue

            except wikipedia.exceptions.DisambiguationError:
                print("disambiguation")
                #page_error.append(term)
                continue 

wiki_extractor(example_list)

print("rate of found pages: "+str(len(dict_companies_pages)/len(example_list)))

f = open("./dict_companies_pages.json", "w+")
json_data = json.dumps(dict_companies_pages)
f.write(json_data)  