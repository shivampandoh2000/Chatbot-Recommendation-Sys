from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
tok = tokenizer.tokenize('Eighty-seven miles to go, yet.  Onward!')
print(tok)
