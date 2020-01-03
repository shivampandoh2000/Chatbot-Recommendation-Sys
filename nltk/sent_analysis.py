import nltk
import pandas as pd
dataset=["Meeting was good","They are quite bad people", "How are you?", "I'm feeling good", "Not so well.", "good", "marvelous","hi","go to hell"]
#dataset = pd.read_csv('/home/shivam007/Downloads/movie_metadata1.csv')
#x=dataset.head()
#print('head ==>\n',x)
nltk.download('vader_lexicon')
def nltk_sentiment(sentence):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    print('sentence ==>', sentence)
    nltk_sentiment = SentimentIntensityAnalyzer()
    score=nltk_sentiment.polarity_scores(sentence)
    print('score ==>', score)
    return score
nltk_results = [nltk_sentiment(row) for row in dataset]
results_df = pd.DataFrame(nltk_results)
text_df = pd.DataFrame(dataset, columns = ['director_name'])
#print('text_df ==>\n', text_df)
nltk_df = text_df.join(results_df)
print(nltk_df)
