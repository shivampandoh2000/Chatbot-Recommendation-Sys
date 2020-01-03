from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from chatterbot import comparisons, response_selection
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words=list(set(stopwords.words("english")))
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import pymongo
import yaml
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["db10"]
mycol = mydb["coll"]
d=[]
for x in mycol.find({},{"_id":0,"Technology \nStack":1,"Solution":1}):
  z={}
  a=x["Technology \nStack"]
  p=a.replace("\n","\\n")
  p=p.lower()
  tok=word_tokenize(p)
  filtered_sent_lst=[]
  for w in tok:
    if w not in stop_words:
      filtered_sent_lst.append(w)
  filtered_sen_tok=' '.join(filtered_sent_lst)
  print('Filtered :',filtered_sen_tok)
  #tok_sen=' '.join(tok)
  #print('Tokenized :',tok_sen)

  # Lemmatization

  wn=WordNetLemmatizer()
  tok_lst_lem=filtered_sen_tok.split()
  lem_lst=[]
  for w in tok_lst_lem:
      lem_lst.append(wn.lemmatize(w))
  filtered_sen_lem=' '.join(lem_lst)
  print('Lemma :',filtered_sen_lem)

  # Removing punctuation and whitespaces
  words=filtered_sen_lem.split()
  table=str.maketrans('','',string.punctuation)
  stripped=[w.translate(table) for w in words]
  for w in stripped:
      if w=="":
          stripped.remove(w)
      elif w==" ":
          stripped.remove(w)
  filtered_sen_pun=' '.join(stripped)
  print('Punc :',filtered_sen_pun)
##############################################
  b=x["Solution"]
  m=b.replace("\n","\\n")
  z["Problem Description"]=filtered_sen_pun
  z["Solution"]=m
  d.append(z)
print("+++++++++++++++++++++++++++++++++++++++++++")
#print(d[0])
for i in d:
  with open('data_base_mix.yml', 'a') as yaml_file:
    yaml.dump(i, yaml_file, default_flow_style=False)
