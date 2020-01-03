import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
stop_words=list(set(stopwords.words("english")))
def textCleaning(dataFrame,columnName):
        corpus = []
        for i in range(0, len(dataFrame)):
            review = re.sub('[^a-zA-Z]', ' ', dataFrame[i])
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
patternDf=pd.DataFrame()
patternDf["information"]=["This query is going for an FTS even though the Indexes are present on the search condition. This contains an implicit data type conversion on indexed column \"USER_ID\". This implicit data type conversion prevents the optimizer from selecting indices on table \"SSOADM\".\"SSO_MODULE_ACCESS_TBL\".\\nCreate a functional index for optimizer to pick up the correct execution plan"]
corpus3=textCleaning(patternDf,'information')
   
cleanedTextDf=pd.DataFrame({'information':corpus3})
#-------------end---------------------


#------------pridect the raw label----------------
rawSeriesvalue=pd.Series(model.predict(corpus3))
#-----------end----------------------
patternDf['label']=rawSeriesvalue.values
ps1 = PorterStemmer()
for i in range (len(patternDf)):
    if(patternDf['label'][i]=='database'):            
        if((ps1.stem('db') in cleanedTextDf['information'][i].lower()) or (ps1.stem('mongodb') in cleanedTextDf['information'][i].lower()) or (ps1.stem('collection') in cleanedTextDf['information'][i].lower()) or (ps1.stem('sql') in cleanedTextDf['information'][i].lower()) or (ps1.stem('table') in cleanedTextDf['information'][i].lower()) or (ps1.stem('database') in cleanedTextDf['information'][i].lower()) or (ps1.stem('mongo') in cleanedTextDf['information'][i].lower()) or (ps1.stem('process') in cleanedTextDf['information'][i].lower()) or (ps1.stem('collection') in cleanedTextDf['information'][i].lower())):
            pass
        else:
            patternDf['label'][i]='unknown'
