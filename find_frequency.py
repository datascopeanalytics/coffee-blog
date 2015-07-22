import re
import csv
from collections import Counter
import random

def clean_text(text):
    for char in '-\\':
        text = text.replace(char,' ')
    return re.findall('[a-z]+', text.lower())

def remove_most_common_words(text):
    number_of_words_to_remove = 10
    most_common_words = []
    word_counter = Counter(text)
    for word in word_counter.most_common(number_of_words_to_remove):
        while word[0] in text:
            text.remove(word[0])
    return text

def get_csv_reader(filename, delim):
    all_rows = []
    with open(filename) as stream:
        stream.readline()
        reader = csv.reader(stream, delimiter=delim)
        for row in reader:
            all_rows.append(row)
    return all_rows

def add_prior(unique_word_list, word_bag):
    for word in unique_word_list:
        word_bag.append(word)
    return word_bag

def generate_random_sentence(word_bag, sentence_length):
    word_count = 0
    random_sentence = []
    #add random words to sentence from all words bag
    while (word_count < sentence_length):
        random_sentence.append(random.choice(word_bag))
        word_count += 1
    return random_sentence

#***************************************************************

filename = "data/coffees_with_origins.csv"
delim = "|"
data = get_csv_reader(filename, delim)

number_of_sentences = 10000
number_of_words_per_sentence = 20

all_words_bag = []
all_unique_words = []
all_regions = []
region_bags = []

for row in data:
    #grab the region and add it to the region list
    origin_country = row[7]
    all_regions.append(origin_country)

    #add the description words to the all_words_bag
    description = row[8]
    description = clean_text(description)
    for word in description:
        all_words_bag.append(word)

all_words_bag = remove_most_common_words(all_words_bag)
all_unique_words = list(set(all_words_bag))
all_unique_words.sort()

# add each unique word one more time for the prior
#all_words_bag = add_prior(all_unique_words, all_words_bag)

#get unique regions
unique_regions = list(set(all_regions))
unique_regions.sort()

#get bag of words for each region
for region in unique_regions:
    words_in_region = []

    #for each row, if the origin matches, then add the description words to the region bag
    for row in data:
        origin_country = row[7]
        if (origin_country == region):
            description = row[8]
            for word in description.split():
                words_in_region.append(word)

    #add all uniques words to region bag for the prior
    #words_in_region = add_prior(all_unique_words, words_in_region)
    region_bags.append([region, words_in_region])

#generate random sentences from all words
sentence_count = 0
total_bag_random_sentences = []
while (sentence_count < number_of_sentences):
    random_sentence = generate_random_sentence(all_words_bag, number_of_words_per_sentence)
    #add entire sentence or array of 10,000 sentences
    total_bag_random_sentences.append(random_sentence)
    sentence_count += 1

#generate random sentences from every region
all_regions_random_sentences = []
for region in region_bags: #this is an array --> [region, words_in_region]
    random_sentences_for_region = []
    sentence_count = 0
    while (sentence_count < number_of_sentences):
        random_sentence = generate_random_sentence(region[1], number_of_words_per_sentence)
        random_sentences_for_region.append(random_sentence)
        sentence_count += 1
    all_regions_random_sentences.append([region[0],random_sentences_for_region])

#check to see if words in region sentences occur more often than in all words bag
all_region_word_scores = []
for region in all_regions_random_sentences:
    relative_word_frequency = {}
    for word in all_unique_words:
        word_score = 0.0
        sentence_count = 0
        while (sentence_count < number_of_sentences):
            region_count = region[1][sentence_count].count(word)
            total_count = total_bag_random_sentences[sentence_count].count(word)
            if(region_count > total_count):
                word_score += 1.0
            # elif(region_count == total_count):
            #     word_score += 0.5
            sentence_count += 1
        final_score = word_score / number_of_sentences * 100
        if (final_score > 1.0):
            relative_word_frequency[word] = round(final_score,2)

    print '******************************************************'
    print region[0], all_regions.count(region[0])
    print '******************************************************'
    print relative_word_frequency
    all_region_word_scores.append([region[0], relative_word_frequency])
