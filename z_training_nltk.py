from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement
import random
import logging
from chatterbot import comparisons, response_selection

import string
# importing NLTK
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words= list(set(stopwords.words("english")))

from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
    
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)

no_res=["Sorry, couldn't answer it.","It seems I am unable to answer it","Out of the Bounds","Not in my scope"]
bot=ChatBot('Basic_Bot',storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            logic_adapters=[
        {
            'import_path':'chatterbot.logic.BestMatch',
            'threshold': 0.60,
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
            'response_selection_method': response_selection.get_most_frequent_response,
            'default_response':'Sorry could not answer.'
        }
        ],database_uri='mongodb://localhost:27017/db12'
            )

trainer=ListTrainer(bot)

for files in os.listdir('/home/shivam007/cht_bot/dbses/'):
    data=open('/home/shivam007/cht_bot/dbses/'+files,'r').readlines()
    print('data ==>', data)
    data_new=[]
    for i in data:
        i=i.lower()
        tok=word_tokenize(i)
        tok_sen=' '.join(tok)
        wn=WordNetLemmatizer()
        tok_lst_lem=tok_sen.split()
        lem_lst=[]
        for w in tok_lst_lem:
            lem_lst.append(wn.lemmatize(w))
        filtered_sen_lem=' '.join(lem_lst)
        print('Lemma :',filtered_sen_lem)
        words=filtered_sen_lem.split()
        table=str.maketrans('','',string.punctuation)
        stripped=[w.translate(table) for w in words]
        for w in stripped:
            if w=="":
                stripped.remove(w)
            elif w==" ":
                stripped.remove(w)
        filtered_sen_pun=' '.join(stripped)
        data_new.append(filtered_sen_pun)

        
    print(data_new)    
    trainer.train(data_new)


while True:
    try:
        print("\n")
        print("You :",end="")
        text=input()
        text=text.lower()
        print(stop_words)
        
        # Tokenization and removing stop words..

        tok=word_tokenize(text)
        #filtered_sent_lst=[]
        #for w in tok:
         #   if w not in stop_words:
          #      filtered_sent_lst.append(w)
        #filtered_sen_tok=' '.join(filtered_sent_lst)
        #print('Filtered :',filtered_sen_tok)
        tok_sen=' '.join(tok)
        #print('Tokenized :',tok_sen)

        # Lemmatization

        wn=WordNetLemmatizer()
        tok_lst_lem=tok_sen.split()
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

        # Lowering the case
        #filtered_sent=filtered_sen_pun.lower()
        input_statement = Statement(filtered_sen_pun)
        print('-'*100)
        print('input_statement ==>', input_statement)
        response = bot.generate_response(
            input_statement
        )
        print('='*100)
        print("Chatbot :",response.text)
    except (KeyboardInterrupt,EOFError,SystemExit):
        break
