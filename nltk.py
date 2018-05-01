# -*- coding: utf-8 -*-
"""
Created on Tue May  1 12:37:37 2018

@author: ee15sjm
"""

import nltk
import pprint
import requests
import time

#set up pretty printer for clearer printing of lists
pp = pprint.PrettyPrinter()

#Open txt file
f = open('WasteLand.txt', encoding='utf8')
text = f.read()
f.close()

#define start position at end of contents
start = 'NOTES ON “THE WASTE LAND”'
start_pos = text.find(start) + len(start)
#define end position at start of "Line 415 aetherial] aethereal"
end_pos = text.find("Line 415 aetherial] aethereal")

#Create a slice between start and end positions
poem = text[start_pos:end_pos]
#print(poem)

#split text in to words
tokens = nltk.word_tokenize(poem)
text = nltk.Text(tokens)
#print(text)

#RUN THE FOLLOWING IN BLOCKS TO PREVENT PLOTTING TO THE SAME GRAPH
"""
#******
#Find 20 most common words
frequency = nltk.FreqDist(text)
pp.pprint(frequency.most_common(20))
#plots to graphs
frequency.plot(20, cumulative=True)
frequency.plot(20)
#******

#******
#Find 20 most common word lengths
length =  nltk.FreqDist(len(word) for word in text)
pp.pprint(length.most_common(20))
#plot to graphs
length.plot(20, cumulative=True)
length.plot(20)
#******

#******
#Find all words over 10 letters
long_words = [word for word in text if len(word) > 10]
pp.pprint(long_words)
#******
"""

#run part-of-speech tagging to ID proper nouns (NNP)
tagged = nltk.pos_tag(text)
#pp.pprint(tagged)

#Seperate text into sentences based on .
sentences = []
sentence = []
for tag in tagged:
    sentence.append(tag)
    if tag[0] == ".":
        sentences.append(sentence)
        sentence = []
        continue
#print(sentences)

grammar = "ProperNouns: {<NNP>}"
chunkparser = nltk.RegexpParser(grammar)

#Filter out proper nouns, remove all caps/punctuation
for sentence in sentences:
    tree = chunkparser.parse(sentence)
    #for subtree in tree.subtrees():
        #if subtree.label()=='ProperNouns': 
            #print(subtree)
p_nouns = []
for sentence in sentences:
    tree = chunkparser.parse(sentence)
    for subtree in tree.subtrees():
        if subtree.label()=='ProperNouns':
            st = str(subtree)
            slash = st.find("/")
            words = st[13:slash] # len of ProperNouns + space
            if words.isupper() == False: #if not all caps
                if words.isalpha() == True: #if only contains letters
                    p_nouns.append(words)
#pp.pprint(p_nouns)

#Geocoding

#References:
#	Based on:
#	https://gist.github.com/pnavarrc/5379521

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?, key="YOUR API KEY"'


for noun in p_nouns:
    #Use each proper noun as an address to search for
    params = {
        'address': noun
    }
    #Request Location info for noun
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()

    #If location is recognised
    if res['results']:
        #Choose first result
        result = res['results'][0]
        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']
        print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
        #Pause for 100 milliseconds to prevent reaching API limit
        time.sleep(.1)
        