import requests
from bs4 import BeautifulSoup
#from urllib.request import urlopen
import os
import re
import string
from collections import OrderedDict

os.chdir('D:/Python_code/Web_Scraping')

def clean_input(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")

    clean_input = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation) # all this !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            clean_input.append(item.title())
    return clean_input

# 2gram
def ngrams_dict(input, n):
    input = clean_input(input)
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i+n])
    return dict(output) # remove dict for more 3gram, 4gram ..

def ngrams_list(input, n):
    input = clean_input(input)
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i+n])
    return output

def check_frequency(input):
    input = clean_input(input)
    output = []
    for dict_item in ngrams_dict.items():
        # dict_item is a tuple
        count = 0
        for item in input:
            if dict_item[0] == item:
                count += 1
        output.append((dict_item, count))
    return output

html = requests.get("http://en.wikipedia.org/wiki/Python_(programming_language)")
bs_obj = BeautifulSoup(html.text, features="lxml")
content = bs_obj.find("div", {"id":"mw-content-text"}).get_text()

ngrams_list = ngrams_list(content, 2)

ngrams_dict = ngrams_dict(content, 2)
ngrams_dict = OrderedDict(sorted(ngrams_dict.items(), key=lambda t: t[1], reverse=True)) # ordering a dict


output = check_frequency(content)
# t deja face referire la un item din lista mea output
# un fel de t[0] unde vreau ca key-ul sa fie t[0][1] adica  t[1]
output = sorted(output, key=lambda t: t[1], reverse = True)
print(output)
print("2-grams count is: " + str(len(ngrams_list)))
print("2-grams unique count is: " + str(len(ngrams_dict)))
