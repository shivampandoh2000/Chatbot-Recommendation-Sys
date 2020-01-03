import sys
sys.path.insert(0, '/home/shivam007/cht_bot/cus_chatterbot')
from chatterbot.chatterbot import ChatBot
#from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ListTrainer
#import webbrowser
import os
#from datetime import datetime
from chatterbot.logic import LogicAdapter
#from chatterbot.conversation import Statement
#from conversation_1 import Statement
from chatterbot.conversation import Statement
#from conversation import Statement
import chatterbot.filters
import re
from chatterbot.trainers import ChatterBotCorpusTrainer
#from chatterbot.storage import StorageAdapter
import pymongo
from custom_mongo import CusMongoDatabaseAdapter

chatbot = ChatBot('Charlie', storage_adapter='custom_mongo.CusMongoDatabaseAdapter',
                  logic_adapters=[{'import_path': 'chatterbot.logic.BestMatch',
                                   'maximum_similarity_threshold':0.7
                                   }
                                  ],
                  database_uri='mongodb://localhost:27017/chatterbot-database7',
                  preprocessors = ['chatterbot.preprocessors.clean_whitespace'],
                  filters = ['filters.get_recent_repeated_responses'],
                  read_only=True)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

while True:
    message = input('You :')
    
    if message.strip() != 'Bye':
        reply=chatbot.get_response(message)
        text = message.strip()
        print('confidence = ', reply.confidence)
         
        if reply.confidence>=0.6:
            print('ChatBot :',reply)
        elif reply.confidence<0.6 :
            #d = 'https://www.google.com/search?client=safari&rls=en&q={0}&ie=UTF-8&oe=UTF-8'.format(message)
            #webbrowser.open_new_tab(d)
            print('Sorry!  no response')  
    elif message.strip()=='Bye':
        print('ChatBot : Bye')
        break
    
''' 
while True:
    try:
        input_statement = Statement(text=input())
        response = chatbot.generate_response(input_statement)
        print('\n Is :"{}" a coherent  response to "{}" ? \n'.format(response.text, input_statement.text))
        if get_feedback(text):
            print('please input the orrect one')
            correct_response = Statement(text = input())
            chatbot.learn_response(correct_response, input_statement)
            print('Responses added to bot!')
    except (KeyboardInterrupt, EOFError, SystemExit):
        break

'''
