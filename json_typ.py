import json



class mydict(dict):
    def __str__(self):
        return json.dumps(self)



couples = {'jack':'ilena'}
pairs = mydict(couples)

print(pairs)
