from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging
from chatterbot import comparisons, response_selection
import webbrowser
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

#--------------This fuction is the main body for Bot---------------------
def database__uri(uri):
    return ChatBot(
        'Feedback Learning Bot',read_only=True,
        storage_adapter='chatterbot.storage.MongoDatabaseAdapter',logic_adapters=[
                        {
                            "import_path": "chatterbot.logic.BestMatch",# used for increasing the accuracy
                            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",#for comparison of two statement
                            "response_selection_method": response_selection.get_most_frequent_response,# gets the most frequent response
                            'threshold': 0.60, #Setting the threshold for comparing two statements
                            'default_response': 'Sorry did not understand. Can be more specific?.'
                        }
                       ],
        preprocessors=[
                        'chatterbot.preprocessors.clean_whitespace'],
        database_uri='mongodb://localhost:27017/'+uri  # Assigning the databse 
                      )#,input_adapter="chatterbot.input.TerminalAdapter",
    #output_adapter="chatterbot.output.OutputAdapter",'''
                
    #trainer=ChatterBotCorpusTrainer(bot)
    #trainer.train(
    #   "chatterbot.corpus.english"
    #)
# -----------------This function could be used as for the feedback purpose-------------
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
        #-----calling the function and giving the database as the argument--------
        bot = database__uri("db20")
        print("\n")
        print("You :",end="")
        #----Taking the input statement from the user------
        text=input()
        text_1=text.lower()
        #print(stop_words)
        
        # Tokenization and removing stop words..

        tok=word_tokenize(text_1)
        filtered_sent_lst=[]
        for w in tok:
            if w not in stop_words:
                filtered_sent_lst.append(w)
        filtered_sen_tok=' '.join(filtered_sent_lst)
        #print('Filtered :',filtered_sen_tok)
        #tok_sen=' '.join(tok)
        #print('Tokenized :',tok_sen)

        # Lemmatization

        wn=WordNetLemmatizer()
        tok_lst_lem=filtered_sen_tok.split()
        lem_lst=[]
        for w in tok_lst_lem:
            lem_lst.append(wn.lemmatize(w))
        filtered_sen_lem=' '.join(lem_lst)
        #print('Lemma :',filtered_sen_lem)

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
        #print('Punc :',filtered_sen_pun)

        # Lowering the case
        #filtered_sent=filtered_sen_pun.lower()
        input_statement = Statement(filtered_sen_pun)
        #print('input_statement ==>', input_statement)
        response = bot.generate_response(
            input_statement
        )
        if response.confidence >=0.6:
            print("Confidence = ",response.confidence)
            print("Chatbot :",response.text)
        else:
            #print("DB ==> db21")
            bot = database__uri("db21")
            import pandas as pd
            from sklearn.pipeline import Pipeline
            from sklearn.pipeline import make_pipeline
            #import nltk
            from nltk.stem import PorterStemmer
            from nltk.tokenize import WhitespaceTokenizer 
            from nltk.tokenize import sent_tokenize, word_tokenize
            from nltk.stem import WordNetLemmatizer
            import re
            #from nltk.corpus import stopwords
            #nltk.download('stopwords')
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.naive_bayes import MultinomialNB
            stop_words = stopwords.words('english')
            
            # for refining the text
            def textCleaning(dataFrame,columnName):
                corpus = []
                for i in range(0, len(dataFrame)):
                    review = re.sub('[^a-zA-Z]', ' ', dataFrame[columnName][i])
                    review = review.lower()
                    review = review.split()
                #----stem is used for root word for ex:- verb3,verb4 etc will goto verb1 
                    ps = PorterStemmer()
                    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
                    review = ' '.join(review)
                    corpus.append(review)
                return corpus




    #---------------fit the traing data-------------------  
    #corpus is just a collection of document(document is nothing but a string which has collection of word )
    # and word is called as token
    #-----READ FROM TRAINED FILE -------------------
            trainingDf1=pd.read_csv('/home/shivam007/Downloads/alertData2.csv')

    #------call text cleaner and fit model-----------------
            corpus=textCleaning(trainingDf1,'alert')
    #convert to new dataframe--------
            trainingDf=pd.DataFrame({'alert':corpus})
            trainingDf['target']=trainingDf1['target']
    #apply NLP and Multinomial naive bayes------
            model = make_pipeline(TfidfVectorizer(), MultinomialNB())
            model.fit(trainingDf.alert,trainingDf.target)

    #---------end of fit model-----------------------

    #------------nlp for prediction------------------
            patternDf = pd.DataFrame()
            #print('filtered_sen_pun ==>', [filtered_sen_pun])
            patternDf['information'] = [filtered_sen_pun]
            corpus3=textCleaning(patternDf,'information')
            #print('corpus3 ==>', corpus3)
            cleanedTextDf=pd.DataFrame({'information':corpus3})
    #-------------end---------------------


    #------------pridect the raw label----------------
            rawSeriesvalue=pd.Series(model.predict(corpus3))
            ly=str(rawSeriesvalue).split("    ")
            #print(str(rawSeriesvalue).split("    "))
            lys=str(ly[1]).split('\n')
            #print("lys ==> ", lys)
            inpt=str(lys[0])
            inpt_stat=Statement(inpt)
            res=bot.generate_response(inpt_stat)
            #-----------end----------------------
          
            if res.confidence>=0.6:
                print("Confidence = ",res.confidence)
                print("Chatbot :",res.text)
            else:
                print("Couldn't find appropriate Solution For the Problem Description.")
                print("These some useful links over Web :")
                try:
                    # this part will bring the top 5 links from the Google
                    from googlesearch import search
                except ImportError:
                    print("No module named 'google' found")
                query = text
                for j in search(query, num=5, stop=5, pause=2):
                    print(j)
                
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
