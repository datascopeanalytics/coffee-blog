# script needs to:
# total bag = get bag of all words + one extra for each word
# region bag = get bag of words for each region + one extra for EVERY word
# for every bag:
#   generate 10,000 sentences of 20 words from every bag
# for every region:
#   for every unique word in the total bag (sort this):
#     find the frequency of that word in each of the 10,000 sentences
#     if the frequency(total_bag) < frequency(region_bag) = 1.0
#     if the frequency(total_bag) = frequency(region_bag) = 0.5
#     if the frequency(total_bag) > frequency(region_bag) = 0.0
#     add up the total (between 0 & 10,000) and divide by 10,000
#       (50% = average, above means greater frequency, lower means less)
#
#     create array of dictionaries
#     [{'Region':'Argentina','words':{'apple':0.75, 'honey':0.82, 'chocolate':0.21},
#
#     print out words in order of likelihood
# make sure words are cleaned up a little

import csv
import random

all_words_bag = []
all_unique_words = []
all_regions = []
region_bags = []
number_of_sentences = 10000
number_of_words_per_sentence = 20

with open("data/coffees_with_origins.csv") as stream:
    stream.readline()
    reader = csv.reader(stream, delimiter="|")

    for row in reader:
        #grab the region and add it to the region list
        origin_country = row[6]
        all_regions.append(origin_country)

        #add the description words to the all_words_bag
        description = row[8]
        for char in '.,\';:!?@#$%^&*()_+{=[]\"}':
            description = description.replace(char,'')
        for char in '-\\':
            description = description.replace(char,' ')
        description = description.lower()
        for word in description.split():
            all_words_bag.append(word)

    all_unique_words = list(set(all_words_bag))
    all_unique_words.sort()

    # add each unique word one more time to have a prior
    for word in all_unique_words:
        all_words_bag.append(word)

    #get unique regions
    unique_regions = list(set(all_regions))
    unique_regions.sort()

    #get bag of words for each region
    for region in unique_regions:
        words_in_region = []

        #for each row, if the origin matches, then add the description words to the region bag
        with open("data/coffees_with_origins.csv") as stream:
            stream.readline()
            reader = csv.reader(stream, delimiter="|")
            for row in reader:
                origin_country = row[6]
                if (origin_country == region):
                    description = row[8]
                    for char in '.,\';:!?@#$%^&*()_+{=[]\"}':
                        description = description.replace(char,'')
                    for char in '-\\':
                        description = description.replace(char,' ')
                    description = description.lower()
                    for word in description.split():
                        words_in_region.append(word)

            #add all uniques words to region bag to have a prior
            for word in all_unique_words:
                words_in_region.append(word)
            region_bags.append([region, words_in_region])

#generate random sentences of 20 words
sentence_count = 0
total_bag_random_sentences = []
while (sentence_count < number_of_sentences):
    word_count = 0
    random_sentence = []

    #add random words to sentence from all words bag
    while (word_count < number_of_words_per_sentence):
        random_sentence.append(random.choice(all_words_bag))
        word_count += 1

    #add entire sentence or array of 10,000 sentences
    total_bag_random_sentences.append(random_sentence)
    sentence_count += 1

#generate random sentences of 20 words for every bag
all_regions_random_sentences = []

for region in region_bags: #this is an array --> [region, words_in_region]
    random_sentences_for_region = []
    sentence_count = 0
    while (sentence_count < number_of_sentences):
        word_count = 0
        random_sentence = []
        #add random words to sentence from all words bag
        while (word_count < number_of_words_per_sentence    ):
            random_sentence.append(random.choice(region[1]))
            word_count += 1
        #add entire sentence or array of 10,000 sentences
        random_sentences_for_region.append(random_sentence)
        sentence_count += 1
    all_regions_random_sentences.append([region[0],random_sentences_for_region])

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
            elif(region_count == total_count):
                word_score += 0.5
            sentence_count += 1
        final_score = word_score / number_of_sentences
        if (final_score > 0.5):
            relative_word_frequency[word] = final_score

    print '******************************************************'
    print region[0], all_regions.count(region[0])
    print '******************************************************'
    print relative_word_frequency
    all_region_word_scores.append([region[0], relative_word_frequency])
