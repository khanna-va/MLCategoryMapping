import json

from sklearn.externals import joblib

classifier = joblib.load('data/pickles/factualCategory.pkl')
factual_tax_json = open('data/factual_taxonomy.json', 'r')

vtax = ['active:bowling', 'active:skatingrinks', 'active:horsebackriding', 'food:grocery',  'financialservices:investing', 'foo']

factual_tax = json.load(factual_tax_json)

predicted = classifier.predict(vtax)

for vt, category in zip(vtax, predicted):
    print('%s => %s - %s' % (vt, category, factual_tax[str(category)]["labels"]["en"]))

