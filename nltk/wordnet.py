import nltk
from nltk.corpus import wordnet
import matplotlib
synonyms = []
antonyms = []

for syn in wordnet.synsets("action"):
    for l in syn.lemmas():
        print(l)
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
print(set(synonyms))
print(set(antonyms))
fq=nltk.FreqDist(synonyms)
print(fq)

