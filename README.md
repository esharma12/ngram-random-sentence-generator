# ngram-random-sentence-generator
1) The problem to be solved in this program is sentence generation using a large corpus of literary text as input. The corpus is at least 1 million words (tokens). Ngram models will be used to assign probability to the occurence of sets of words from the set, the length of the sets being n. The program creates Ngram tables of all the possible ngrams in the corpus along with the probability of seeing that Ngram. If the program is to run a 3-gram (trigram), the program will parse the text to generate the trigrams, and then calculate the probabiltiy of the trigrams using previously calculated probability history of the n-1(bigrams) of the corpus. The program outputes m generated sentences from the Ngram model of the corpus. The input for the program are n for the level of the ngrams (bi, tri, ...), m for # of sentences, and the names of the corpus text files to be used. The Ngram model can be trained using any corpus, but when creating this project, I used fictional texts from Project Gutenberg. Specifically, I used 'Sense and Sensibility', 'Emma', and 'Pride and Prejudice' by Jane Austen.
2) Examples of program input are: ngram.py 3 10 emma.txt pride.txt sense.txt, or ngram.py 5 15 emma.txt pride.txt sense.txt. Examples of outputted sentences include :
"Indeed I after some be increased well looking; came away only indifferent her out are single, her intentions his resentment."
"Mrs weston you upon unsuitable it asked for of friends company the instant return if possible it sent away abbey …  a kindly given vex her right number"
Usage instructions: python3.11 ngram.py n m filename.txt
