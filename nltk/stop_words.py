import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))
print(stop_words)
sen="Hi how , are ,  you,  bye, I an me with you..."
tok=word_tokenize(sen)
filtered_sent=[]
for w in tok:
    if w not in stop_words:
        filtered_sent.append(w)
print("\n")
print("Tokenized Sentence:",tok,"\n")
print("Filterd Sentence:",filtered_sent)
