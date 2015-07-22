import re
import csv
import collections
import numpy
import operator

#stopwords from http://xpo6.com/list-of-english-stop-words/
stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

def clean_text(text):
    for char in '-\\':
        text = text.replace(char,' ')
    return re.findall('[a-z]+', text.lower()) #returns an array of words that fit regex

def get_csv_reader(filename, delim):
    all_rows = []
    with open(filename) as stream:
        stream.readline()
        reader = csv.reader(stream, delimiter=delim)
        for row in reader:
            all_rows.append(row)
    return all_rows                          #returns an array of all rows in csv

def remove_stopwords(words):
    return set(words) - set(stopwords)

def bag_of_words_not_in_set(words, badwords):
    return bag_of_words(set(words) - set(badwords))

def calculcate_word_significance(category_counter, prior, min_count):
    prior = 0
    array_of_words = []
    for region, counter in category_counter.iteritems():
        n_in_category = sum(counter.values())
        n_words_in_category = len(counter)
        n_in_all = sum(all_words_counter.values())
        n_words_in_all = 0 #len(all_words_counter)
        for word, count in counter.iteritems():
            if (count >= min_count):
                log_of_total_count = numpy.log(all_words_counter[word])
                ratio_in_category = float(count+prior)/(n_in_category+n_words_in_all)
                ratio_in_total = float(all_words_counter[word]+prior)/(n_in_all+n_words_in_all)
                significance = log_of_total_count * ratio_in_category / ratio_in_total
                if (region != "NA"):
                    array_of_words.append([region, word, round(significance,2)])
    return array_of_words

def sort_by_column(column_number,item):
    return item[column_number]

def append_to_csv(filename, write_type, data_list, delim):
    out = csv.writer(open(filename, write_type), delimiter=delim,quoting=csv.QUOTE_ALL)
    try:
        out.writerow(data_list)
    except:
        print "Error writing to csv."

#***************************************************************

filename = "data/coffees_with_regions.csv"
delim = "|"
data = get_csv_reader(filename, delim)

all_regions = []
all_roasts = []
all_words = []
all_words_counter = collections.Counter()
region_word_counter = collections.defaultdict(collections.Counter)
roast_word_counter = collections.defaultdict(collections.Counter)

for row in data:
    #add the description words to the all_words_bag
    description = row[-1]
    description = clean_text(description)
    description = remove_stopwords(description)
    for word in description:
        all_words.append(word)

#find words that exist without suffix
one_letter_stem = []
two_letter_stem = []
three_letter_stem = []
unique_words = set(all_words)
for word in unique_words:
    if (word[-1] == 'y' or word[-1] == 's'):
        if (word[:-1] in unique_words):
            one_letter_stem.append(word)
    if (word[-2:] == 'ly' or word[-2:] == 'ed'):
        if (word[:-2] in unique_words):
            two_letter_stem.append(word)
    if (word[-3:] == 'ing'):
        if (word[:-3] in unique_words):
            three_letter_stem.append(word)

all_words = []
for row in data:
    #clean description text
    description = row[-1]
    description = clean_text(description)
    description = remove_stopwords(description)

    #grab the categories
    region = row[-3]
    all_regions.append(region)
    roast = row[-2]
    all_roasts.append(roast)

    for word in description:
        #get rid of suffixes that make duplicates
        if word in one_letter_stem:
            word = word[:-1]
        if word in two_letter_stem:
            word = word[:-2]
        if word in three_letter_stem:
            word = word[:-3]
        all_words.append(word)
        all_words_counter[word] += 1
        region_word_counter[region][word] += 1
        roast_word_counter[roast][word] += 1

#print list of top 50 words raw
print all_words_counter.most_common(50)
for word, count in all_words_counter.most_common(50):
    append_to_csv('data/top_50_words_raw.csv', 'a+',[word, count],',')

# remove most common words
number_of_words_to_remove = 20
for word in all_words_counter.most_common(number_of_words_to_remove):
    word_to_remove = word[0]
    del all_words_counter[word_to_remove]
    for region, counter in region_word_counter.iteritems():
        del counter[word_to_remove]
    for roast, counter in roast_word_counter.iteritems():
        del counter[word_to_remove]

#set up csvs for new data
append_to_csv('categories/region_words2.csv', 'w', ["region","word","score"], '|')
append_to_csv('categories/roast_words2.csv', 'w', ["roast","word","score"], '|')

#loop through every word in every region and calculate ...
#log(word count in big bag) x (ratio of word count in region bag) / (ratio of word count in big bag)
prior = 1
min_count = 2

#regions
region_words_set = []
region_words = calculcate_word_significance(region_word_counter, prior, min_count)
region_words = sorted(region_words, key=operator.itemgetter(2), reverse = True)
for row in region_words:
    #add words in region to csv if word is not in another region
    if row[1] in region_words_set:
        del row
        continue
    else:
        region_words_set.append(row[1])

    region = row[0]
    word = row[1]
    score = row[2]

    append_to_csv('categories/region_words2.csv', 'a+', row, '|')
    append_to_csv('categories/'+ region + '_words2.csv', 'a+', row, '|')

    # print region, word, score, region_word_counter[region][word]

#roasts
roast_words_set = []
roast_words = calculcate_word_significance(roast_word_counter, prior, min_count)
roast_words = sorted(roast_words, key=operator.itemgetter(2), reverse = True)
for row in roast_words:
    #add words in roast to csv if word is not in another roast yet
    if row[1] in roast_words_set:
        del row
        continue
    else:
        roast_words_set.append(row[1])

    roast = row[0]
    word = row[1]
    score = row[2]

    append_to_csv('categories/roast_words2.csv', 'a+', row, '|')
    append_to_csv('categories/'+ roast + '_words2.csv', 'a', row, '|')

    # print roast, word, score, roast_word_counter[roast][word]
