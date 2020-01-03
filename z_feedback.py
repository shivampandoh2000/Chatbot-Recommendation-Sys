from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from chatterbot import comparisons, response_selection

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.INFO)

import string
# importing NLTK

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words= list(set(stopwords.words("english")))

from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer



# Create a new instance of a ChatBot
bot = ChatBot(
    'Feedback Learning Bot',read_only=True,
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',logic_adapters=[
                    {
                        "import_path": "chatterbot.logic.BestMatch",
                        "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                        "response_selection_method": response_selection.get_most_frequent_response,
                        'threshold': 0.60,
                        'default_response': 'Sorry did not understand. Can be more specific?.'
                    }
                   ], preprocessors=[
                    'chatterbot.preprocessors.clean_whitespace'],database_uri='mongodb://localhost:27017/db11'
               )#,input_adapter="chatterbot.input.TerminalAdapter",
#output_adapter="chatterbot.output.OutputAdapter",'''
                
#trainer=ChatterBotCorpusTrainer(bot)
#trainer.train(
#   "chatterbot.corpus.english"
#)



def get_feedback():

    text = input()

    if 'yes' in text.lower():
        return False
    elif 'no' in text.lower():
        return True
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        print("\n")
        print("You :",end="")
        text=input()

        input_statement = Statement(text)
        print('-'*100)
        print('input_statement ==>', input_statement)
        response = bot.generate_response(
            input_statement
        )
        print('='*100)
        print("Chatbot :",response.text)
        
        print('\n Is "{}" a coherent response to "{}"? \n'.format(
            response.text,
            input_statement.text
        ))
        if get_feedback():
            print('please input the correct one')
            correct_response = Statement(text=input())
            bot.learn_response(correct_response, input_statement)
            print('Responses added to bot!')

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
