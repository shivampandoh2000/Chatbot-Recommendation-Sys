from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot=ChatBot('Bot',logic_adapters=['chatterbot.logic.BestMatch'])
trainer=ListTrainer(bot)

data=open('/home/shivam007/chatterbot-corpus/chatterbot_corpus/data/english/ai.yml','r').readlines()
trainer.train(data)

while True:
    message = input('You:')
    if message.strip() != 'Bye':
        reply=bot.get_response(message)
        print('ChatBot :',reply)
    if message.strip()=='Bye':
        print('ChatBot :Bye')
        break

