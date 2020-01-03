from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import random

def get_feedback():

    text = input()

    if 'yes' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


no_res=["Sorry, couldn't answer it.","It seems I am unable to answer it."]
bot=ChatBot('Main_Bot',read_only=True,
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            logic_adapters=[
            {
                'import_path':'chatterbot.logic.BestMatch',
                'maximum_similarity_threshold':0.90,
                #'excluded_words':'["Artificial"]',
                'input_text':'Hi',
                'output_text':'Hi there',
                'default_response':'I am sorry, but I do not understand.'
            },
            {'import_path':'chatterbot.logic.MathematicalEvaluation'},
            {'import_path':'chatterbot.logic.SpecificResponseAdapter',
             'input_text':'Hi',
             'output_text':'Hi there'
             }],database_uri='mongodb://localhost:27017/db14'
    )

trainer=ListTrainer(bot)


for files in os.listdir('/home/shivam007/cht_bot/dbses/dses_1/'):
    data=open('/home/shivam007/cht_bot/dbses/dses_1/' + files ,'r').readlines()
    trainer.train(data)



while True:
    message = input('You :')
    if message.strip() != 'Bye' or message.strip() != 'bye':
        reply=bot.get_response(message)
        print('confidence =', reply.confidence) 
        print('ChatBot :',reply)
    elif message.strip()=='Bye' or message.strip()=='bye':
        print('ChatBot :Bye')
        break
