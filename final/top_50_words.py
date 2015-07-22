import csv
import json
import collections
import re

def get_csv_reader(filename, delim):
    all_rows = []
    with open(filename) as stream:
        stream.readline()
        reader = csv.reader(stream, delimiter=delim)
        for row in reader:
            all_rows.append(row)
    return all_rows                       #returns an array of all rows in csv

def clean_text(text):
    for char in '-\\':
        text = text.replace(char,' ')
    return re.findall('[a-z]+', text.lower()) #returns an array of words that fit regex

filename = "data/coffees_with_regions.csv"
json_file = open("data/top_50_words_raw.json", "w")

delim = "|"
data = get_csv_reader(filename, delim)

all_words_counter = collections.Counter()

for row in data:
    description = row[-1]
    description = clean_text(description)
    for word in description:
        all_words_counter[word] += 1


with json_file as outfile:
    for word in all_words_counter.most_common(50):
        json_data = {}
        json_data["name"] = word[0]
        json_data["size"] = word[1]
        json.dump(json_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        outfile.write(",\n")
