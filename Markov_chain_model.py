import random
import requests

def word_list_sum(word_list):
    sum = 0
    for word, value in word_list.items():
        sum += value
    return sum

def retrieve_random_word(word_list):
    rand_index = random.randint(1, word_list_sum(word_list))
    for word, value in word_list.items():
        rand_index -= value
        if rand_index <= 0:
            return word

def build_word_dict(text):
    #Remove newlines and quotes
    text = text.replace('\n', ' ')
    text = text.replace('\"', '')

    #Makeing sure punctuation marks are treated as their own "words,"
    #so that they will be included in the Markov chain
    punctuation = [',', '.', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, ' ' + symbol + ' ')

    words = text.split(' ')

    #Filter out empty words
    words = [word for word in words if word != '']

    word_dict = {}
    for i in range(1, len(words)):
        if words[i-1] not in word_dict:
            #Create a new dictionary for this word
            # { key = words[i-1], value = {} }
            word_dict[words[i-1]] = {}
        # If the second word is not in { word[i-1]:{ word_A:0, word_B:0 ..} }
        if words[i] not in word_dict[words[i-1]]:
            word_dict[words[i-1]][words[i]] = 0
        word_dict[words[i-1]][words[i]] += 1
    return word_dict

text = requests.get('http://pythonscraping.com/files/inaugurationSpeech.txt').text
word_dict = build_word_dict(text)

#Generate a Markov chain of length 100
length = 100
chain = ''
current_word = 'I'
for i in range(0, length):
    chain += current_word + ' '
    # choses from { 'I': {'am':5, 'was':7, ...},
    #               'am': {'cool':3, 'done':6, 'playing':8},
    #               'playing': {'football':5, 'volleyball':2} }
    current_word = retrieve_random_word(word_dict[current_word])

print(chain)
