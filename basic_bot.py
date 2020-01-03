

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import random


###############################################################################################


# chatterbot.logic.logic_adapter


from chatterbot.adapters import Adapter
from chatterbot.storage import StorageAdapter
from chatterbot.search import IndexedTextSearch
from chatterbot.conversation import Statement



    
# chatterbot.logic.best_match



from chatterbot.logic import LogicAdapter
from chatterbot import filters



# chatterbot.logic.time_adapter



from datetime import datetime
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement





no_res=["Sorry, couldn't answer it.","It seems I am unable to answer it","Out of the Bounds","Not in my scope"]
bot=ChatBot('Basic_Bot',storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            logic_adapters=[
        {
            'import_path':'chatterbot.logic.BestMatch',
            'maximum_similarity_threshold': 0.90,
            #'excluded_words':'["Artificial"]',
            'input_text': 'Hi',
            'output_text':'Hi there',
            'default_response': 'I am sorry, but I do not understand.'
        },
        {'import_path':'chatterbot.logic.MathematicalEvaluation'},
        {'import_path':'chatterbot.logic.SpecificResponseAdapter',
         'input_text':'Hi',
         'output_text':'Hi there'
         }
        ],database_uri='mongodb://localhost:27017/db1'
            )
trainer=ListTrainer(bot)


for files in os.listdir('/home/shivam007/chatterbot-corpus/chatterbot_corpus/data/english/'):
    data=open('/home/shivam007/chatterbot-corpus/chatterbot_corpus/data/english/' + files ,'r').readlines()
    trainer.train(data)



while True:
    message = input('You :')
    if message.strip() != 'Bye':
        reply=bot.get_response(message)
        print('confidence =', reply.confidence) 
        print('ChatBot :',reply)
    elif message.strip()=='Bye':
        print('ChatBot :Bye')
        break
