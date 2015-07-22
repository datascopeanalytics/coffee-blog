import csv
import collections

#list of countries and regions that grow coffee
country_list = ['Brazil','Colombia','Indonesia','Ethiopia','India','Mexico','Guatemala','Peru','Honduras',
'Uganda','Nicaragua','Ecuador','Thailand','Tanzania','Kenya','Philippines','Burundi','Haiti','Rwanda','Bolivia','Zambia','Panama','United_States','Jamaica',
'Malawi','El_Salvador','Costa_Rica','Dominican_Republic','Democratic_Republic_Of_The_Congo','Not_Disclosed',
'Hawaii','South_America','Latin_America','Central_Africa','Taiwan','Puerto_Rico','Central_America','Timor',
'Yemen','China','East_Africa','Zimbabwe','Papua_New_Guinea','Australia','Africa']

#map countries to coffee regions
regions = {
"CentralAmerica_Mexico":['Mexico','Guatemala','Honduras','Nicaragua','El_Salvador','Costa_Rica','Panama','Latin_America','Central_America'],
"Caribbean":['Dominican_Republic','Jamaica','Haiti','Puerto_Rico'],
"South_America":['Brazil','Colombia','Peru','Ecuador','Bolivia','South_America'],
"Africa":['Ethiopia','Uganda','Tanzania','Kenya','Burundi','Democratic_Republic_Of_The_Congo','Malawi','Zambia','Rwanda','Central_Africa','East_Africa','Zimbabwe','Africa'],
"Asia_Indonesia":['Indonesia','India','Thailand','Philippines','Taiwan','Timor','Yemen','China','Papua_New_Guinea','Australia'],
"Hawaii":['Hawaii','United_States']
}

def append_to_csv(filename, write_type, data_list):
    out = csv.writer(open(filename, write_type), delimiter='|',quoting=csv.QUOTE_ALL)
    try:
        out.writerow(data_list)
    except:
        print "Error writing to csv."

#create new csv with region header
filename = 'data/coffees_with_regions.csv'
csv_headers = ['coffee', 'company', 'rating', 'city', 'state', 'origin','origin_country', 'region','roast', 'description']
append_to_csv(filename, 'w', csv_headers)

#populate dictionary of coffee countries
coffee_countries = {}
for country in country_list:
    coffee_countries[country] = 0

#read from raw coffee review data
final_coffees = []
raw_data_file = "data/coffee_reviews.csv"
with open(raw_data_file) as stream:
    stream.readline()
    reader = csv.reader(stream, delimiter="|")

    #find countries in origins
    for row in reader:
        origin = row[5]

        #clean up origin text
        for char in '.,\';:!@#$%^&*()_+=[]{}"':
            origin = origin.replace(char, '')

        #remove spaces in the countries we want to keep track of
        origin = origin.replace('El Salvador', 'El_Salvador')
        origin = origin.replace('Costa Rica', 'Costa_Rica')
        origin = origin.replace('Puerto Rico', 'Puerto_Rico')
        origin = origin.replace('Papua New Guinea', 'Papua_New_Guinea')
        origin = origin.replace('Dominican Republic', 'Dominican_Republic')
        origin = origin.replace('Democratic Republic of the Congo', 'Democratic_Republic_Of_The_Congo')
        origin = origin.replace('Central African Republic', 'Central_African_Republic')
        origin = origin.replace('Trinidad and Tobago', 'Trinidad_And_Tobago')
        origin = origin.replace('RepublicoftheCongo', 'Republic_Of_The_Congo')
        origin = origin.replace('Latin America', 'Latin_America')
        origin = origin.replace('South America', 'South_America')
        origin = origin.replace('Central America', 'Central_America')
        origin = origin.replace('Eastern Java', 'Indonesia')
        origin = origin.replace('East Africa', 'East_Africa')
        origin = origin.replace('Central Africa', 'Central_Africa')
        origin = origin.replace('United States', 'United_States')
        origin = origin.replace('Not disclosed', 'Not_Disclosed')

        #count number of countries in origin; only keep those with one
        number_of_countries = 0
        for word in origin.split():
            if(word in country_list):
                number_of_countries += 1

        #find region
        for word in origin.split():
            if(word in country_list):
                for key, values in regions.iteritems():
                    for country in values:
                        if country == word:
                            current_region = key

                #add row to CSV if there is only one country AND it's not 'Not Disclosed'
                if(number_of_countries == 1 and word != 'Not_Disclosed'):
                    country = word
                    new_coffee_row = [row[0],row[1],row[2],row[3],
                    row[4],row[5],country,current_region,row[6],row[7]]
                    append_to_csv(filename, 'a+', new_coffee_row)

                    final_coffees.append(new_coffee_row)

# print final_coffees
print "Final Coffee Review Count: ", len(final_coffees)
