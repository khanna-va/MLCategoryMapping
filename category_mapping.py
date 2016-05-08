import numpy as np
import csv
import json
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.preprocessing import MultiLabelBinarizer



training_data_csv = open('data/2000ActiveFactualOut.csv', 'r', encoding='utf-8', errors='ignore')
factual_tax_json = open('data/factual_taxonomy.json')
outfile = open('data/mapped_categories.csv', 'w')


fieldnames = ("vtax","eid","ag_account","website", "company_name", "factual_category_ids")
training_data_reader = csv.DictReader(training_data_csv, fieldnames)

factual_tax = json.load(factual_tax_json)

#print(factual_tax["1"]["labels"]["en"])

vtaxes = []
fids = []
unique_vtaxes = set()

out = []

for row in training_data_reader:
    if row['factual_category_ids']:
        vtax = row['vtax']
        fid = row['factual_category_ids']

        vtaxes.append(vtax)
        fids.append(fid)
        unique_vtaxes.add(vtax)

X_train = np.array(vtaxes)
y_train = fids
X_test = unique_vtaxes


classifier = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])

classifier.fit(X_train, y_train)

predicted = classifier.predict(X_test)


print(predicted)
print(X_test)

for item, labels in zip(X_test, predicted):
    tmp_fid = factual_tax[str(labels)]["labels"]["en"]
    out.append([item, labels, tmp_fid])
    print('%s => %s - %s' % (item, labels, tmp_fid))

writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
writer.writerows(out)