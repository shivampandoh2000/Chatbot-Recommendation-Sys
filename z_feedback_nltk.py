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
                    'chatterbot.preprocessors.clean_whitespace'],database_uri='mongodb://localhost:27017/db12'
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
        text=text.lower()
        print(stop_words)
        
        # Tokenization and removing stop words..

        tok=word_tokenize(text)
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
