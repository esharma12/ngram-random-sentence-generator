    # Esha Sharma 02/19/24 CMSC 416 PA2
# 1) The problem to be solved in this program is sentence generation using a large corpus of literary text as input. The corpus is at least 1 million words (tokens). Ngram models will be used to assign probability to the occurence of
# sets of words from the set, the length of the sets being n. The program creates Ngram tables of all the possible ngrams in the corpus along with the probability of seeing that Ngram. If the program is to run a 3-gram (trigram), the program
# will parse the text to generate the trigrams, and then calculate the probabiltiy of the trigrams using previously calculated probability history of the n-1(bigrams) of the corpus. The program outputes m generated sentences from the Ngram model of the corpus. The input
# for the program are n for the level of the ngrams (bi, tri, ...), m for # of sentences, and the names of the corpus text files to be used.
# 2) # Examples of program input are: ngram.py 3 10 emma.txt pride.txt sense.txt, or ngram.py 5 15 emma.txt pride.txt sense.txt
# Examples of outputted sentences include : 
# "Indeed I after some be increased well looking; came away only indifferent her out are single, her intentions his resentment."
# "Mrs weston you upon unsuitable it asked for of friends company the instant return if possible it sent away abbey …  a kindly given vex her right number"
# Usage instructions: python3.11 ngram.py n m filename.txt
# 3) The algorithm I have used can be described as following: First, the corpus texts files are read into one string. The string is then sent
# to a preprocess function to be sanitized, cleaned up of double quotation marks and symbols in the text files that should not be considered as a token like _. 
# Mr. and Mrs. is also replaced with Mr and Mrs to not allow those period to become end of sentence demarkers. The string is converted to all lowercase, and a whitespace is added
# between the last word of a sentence and the puncuation to treat the puncuation as its own token. Then, the sanitized and tokenized corpus is converted into a unidictionary 
# that includes the frequency of every token in the corpus and the token itself. This is a generalized process because regardless of n,
# a unidictionary will be needed. If n = 1, the unigram generated sentences are done in their own method. To generate these sentences, a random number is used to select to "next" unigram to add to the sentence
# to be generated. If the probability of that token is greater than the random number, then it is appended to the output sentence. Once the end tag <END>, is seen,
# the sentence generation is stopped and sentence is returned to main. The puncuatation is hard coded as well. If n > 1, then the unidictionary is added into a nested dictionary called nestedDict.
# The untokenized text string is sent into the function, generate Ngrams, where you enter a loop that starts from 2 (the lowest ngram besides 1), and ranges to n + 1.
# This is to account for n itself. In the first loop, the text string is sent to the function tagify for n - 1 <START> tags to be added to every sentence. So, a n-1 start tags
# are added to the beginning of the entire corpus text, and then puncuation throughout the corpus is replaced with 'puncuation' + <END>  + n-1 start tags. Then, the tokenized ngram dict is sent into 
# a function that calculates the probability of that ngram based on the history of the n-1 gram. After the dictionary is filled with all of the probabilities, 
# the dictionary is sent to the generateNgramSentences function where it loops through the dictionary of ngrams and probabiltiies. First, it looks for
# an ngram that has n-1 start tags and appends that ngram to the array where the sentence is built. As it iterates through the dictionary, it reassigns
# the random number and the lastNgram variable which contains the last "word" in the last ngram found and added to the sentence array. Once the end tag "<END>"
# is seen in the sentence array, the loop is broken out of, the sentence is cleaned up and returned. This repeats m times. 

import sys
import random
import re
from collections import Counter
from pprint import pprint 
def main():
    fileNames = ''
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    for i in range(3, len(sys.argv)):
        fileNames += sys.argv[i] + ' '
    print('%python',sys.argv[0],n,m,fileNames)
    print('This program generates random sentences based on an Ngram model')
    print('Author: Esha Sharma')
    print('Command line settings :',sys.argv[0],n,m)
    corpusTexts = ""
    #read in all of the corpus into one string
    for text in sys.argv[3:]:
        with open(text, "r", encoding="utf-8") as file:
            corpusTexts += file.read()
    #sanitize and tokenize corpus mainly for unigram work
    # s is list of separated tokens corpusText is string
    s = preprocess(corpusTexts)
    corpusTexts = ' '.join(s)
    uniDict = generateUnigrams(s, n)
    nestedDict = {}
    #unigrams
    if n == 1:
        for m in range(0, m):
            sentence = generateUnigramSentence(uniDict)
            print(sentence)
    #ngrams
    else:
        nestedDict.update({'1' : uniDict})
        nestedDict = generateNgrams(s, n, nestedDict, corpusTexts)
        #pprint(nestedDict)
        for m in range(0, m):
            for m in range(0, m):
                sentence = generateNgramSentence(nestedDict, n)
                print(sentence)
#preprocess corpus to remove unwanted symbols/puncuation, lowercase it, and tokenize puncuation by adding spaces
def preprocess(corpusTexts):
    corpusTexts = corpusTexts.lower()
    corpusTexts = re.sub(r"\b(mr?)\.", r"\1", corpusTexts)
    corpusTexts = re.sub(r"\b(mrs?)\.", r"\1", corpusTexts)
    corpusTexts = re.sub(r"['\"“”‘’„”«»,]", '', corpusTexts) 
    corpusTexts = corpusTexts.replace('_', '')
    s = re.findall(r"[\w']+|[.,!?;]", corpusTexts)  
    return s
#this method generates the probabiltiies of each token in the corpus by using the total amount of tokens, returns dict with unigram keys and prob values
def generateUnigrams(s, n):
    uniDict = {}
    for token in s:
        if token not in uniDict:
            uniDict[token] = 1
        else:
            uniDict[token] += 1
    corpusTotal = sum(uniDict.values())
    probability = 0
    for token, freq in uniDict.items():
        probability += freq/corpusTotal
        uniDict[token] = probability    
    return uniDict
#this method takes in the string, not list, or corpus, first adds n-1 start tags and then "tokenizes" corpus with start and end tags into list
# two loops, outer loop is for generating ngrams from 2 to n, for loop inside is to call tagify for n-1 start tags
# zip is used to turn the gramtokens into one large dict, Counter is used to count frequencies, and then dict is transformed into regular dict
#the nested dict is updated with the ngram dict, and then passes it into the function that calculates probability from frequencies 
def generateNgrams(s, n, nestedDict, texts): 
    d = {} 
    ngrams = []
    for i in range(2, n + 1):             
        for k in range(i - 1):
            tokens = tagify(i, texts)
        gramTokens = [tokens[j: ] for j in range (0, i)]
        ngrams =  zip(*gramTokens)
        d = Counter(ngrams)
        dict(d)
        nestedDict.update({n : d})
        nestedDict = getNgramProbability(nestedDict)
    #returned to main
    return nestedDict

#calculates probability of all ngrams from frequency history and returns the nested dict to function generateNgrams after done
def getNgramProbability(nestedDict):
    for n, d in nestedDict.items():
        total = 0
        probability = 0
        for key in d:
            total += d[key]
        for key in d:
            probability += d[key]/total
            d[key] = probability
    return nestedDict
# this method generates sentences for unigrams by comparing probability of a unigram token to generated random number, once puncuation is hit, for loop is broken out of,
#and sentenceArray is changed to a string, puncuation is hardcoded, and sentence is returned.
def generateUnigramSentence(uniDict):
    sentenceArray = []
    randomNumber = random.random()
    for token, probability in uniDict.items():
        if  probability >= randomNumber:
            randomNumber = random.random()
            sentenceArray.append(token)
            if token == '.' or token == '!' or token == '?':
                break
    sentence = " ".join(sentenceArray)
    sentence = sentence + "."
    return sentence.capitalize()

# this method generates sentences based on given n for the ngrams. it loops through the n dict for the ngrams, and only appends an ngram after it is chosen through
# some parameters. the generated random number should be less than the probabiltiy of the ngram, but the chosen ngram should start with the last "word"
# of the last ngram chosen. once the end tag is seen in the sentence array, the loop is broken out of and the sentence is cleaned by removing start and end tags/
def generateNgramSentence(nestedDict, n):
    nestedDict = dict(nestedDict)
    sentenceArray = []
    sentence = ""
    for i in range(n - 1):
        sentenceArray.append("<START>")
    lastNgram = str(sentenceArray[-1])
    randomNumber = random.random()
    for ngram, probability in nestedDict[n].items():
        if probability > randomNumber and lastNgram in str(ngram): 
                sentenceArray.append(ngram)
                lastNgram = str(sentenceArray[-1])
                if "<END>" in sentenceArray:
                    break;
    sentence = " ".join(" ".join(elems) for elems in sentenceArray)
    sentence = sentence.replace("<START>", " ")
    sentence = sentence.replace("< S T A R T >", " ")
    sentence = sentence.replace("<END>", ".")
    return sentence
#adds n-1 start tags and end tags throughout corpus, string is converted to list and returned
def tagify(i, texts):
    startTag = ""
    for i in range(i - 1):
        startTag = startTag + "<START>"
    texts = startTag + texts
    startTag = "<END>" + startTag
    texts = texts.replace(".", "." + startTag)
    texts = texts.replace("!", "!" + startTag)
    texts = texts.replace("?", "?" + startTag)
    return texts.split()

if __name__ == "__main__":
    main()