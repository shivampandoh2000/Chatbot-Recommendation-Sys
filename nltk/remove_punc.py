
n="}} Hi my. is Shivam }}?"
words = n.split()
# remove punctuation from each word
import string
table = str.maketrans('', '', string.punctuation)
print(table)
print("======================================")
stripped = [w.translate(table) for w in words]
print(stripped)
