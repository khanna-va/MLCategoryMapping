import csv

from factual import Factual

csvfile = open('data/5000MiscFactual.csv', 'r', encoding='utf-8', errors='ignore')
outfile = open('data/5000MiscFactualMapped.csv', 'w')

#https://factual.com/keys
factual = Factual('foo', 'bar')

def get_factual_category( factual_id ):
    try:
        data = factual.get_row('places', factual_id)
        return data["category_ids"]
    except:
        print('excption: ' + factual_id)
        return []


fieldnames = ("vtax","eid","ag_account","website", "company_name", "factual_category_ids")
reader = csv.DictReader( csvfile, fieldnames)
out = []

for row in reader:
    vtax = eval(row['vtax'])[0]

    if not row['factual_category_ids']:
        tmp_factual_category_ids = get_factual_category( row['eid'] )
        if tmp_factual_category_ids:
            factual_category_ids = tmp_factual_category_ids[0]
        else:
            factual_category_ids = None

    else:
        factual_category_ids = eval(row['factual_category_ids'])[0]

    line = [vtax, row['eid'], row['ag_account'], row['website'], row['company_name'], factual_category_ids]
    print(line)
    out.append(line)


writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)
writer.writerows(out)


