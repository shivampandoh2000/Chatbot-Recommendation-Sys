import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk import RegexpParser
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

sen="Apple a day keeps doctor away."
tok=word_tokenize(sen)
print("Tokens = ",tok)
print("\n")
tags=pos_tag(tok)
print("Tags = ",tags)
print("\n")
ps=PorterStemmer()

wn=WordNetLemmatizer()

# STEMMING EXAMPLE

print("Examples of Stemming are :-")
for w in tok:
    print("After Stemming: {} => {}".format(w,ps.stem(w)))
print("\n")

# LEMMATIZATION EXAMPLE

print("Examples of Lemmatization are :-")
for w in tok:
    print("Lemma of {} is {}".format(w,wn.lemmatize(w)))
