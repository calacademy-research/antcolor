from collections import Counter
import csv

bigstring = "";

with open('microhabUncat.csv', encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(row[2] != "None"):
            bigstring = bigstring + "" + str(row[2])

split = bigstring.split()
counts = Counter(split)
mostcommon = counts.most_common(60)
print(mostcommon)

