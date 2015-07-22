import requests
import csv
import pickle
from bs4 import BeautifulSoup

def get_content_from_review_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url,headers=headers)
    soup = None
    if r.ok:
        soup = BeautifulSoup(r.content)
    else:
        print('could not open %s: %s',url, r.status_code)
    return soup

def extract_info_from_review(souped_content):
    company_name = souped_content.find('h3').text.strip().encode('utf8')
    try:
        review_info = []
        coffee_name = souped_content.find('h2', {'class':'review-title'}).text.strip().encode('utf8')
        rating = souped_content.find('div',{'class':'review-rating'}).text.strip()
        souped_info =  souped_content.find_all('p')
        location = souped_info[0].text.strip().encode('utf8')
        origin = souped_info[1].text.strip().encode('utf8')
        roast = souped_info[2].text.strip().encode('utf8')
        description = souped_info[12].text.strip().encode('utf8')
        location = location[10:]
        location = location.split(',')
        city = location[0].strip()
        state = location[1].strip()
        origin = origin[8:].strip()
        if origin[-1] == '.':
            origin = origin[0:-1]
        roast = roast[7:].strip()

        review_info = [coffee_name, company_name, rating, city, state, origin, roast, description]
        return review_info
    except:
        print "Error extracting info from review for" + company_name

def append_to_csv(filename, write_type, data_list):
    out = csv.writer(open(filename, write_type), delimiter='|',quoting=csv.QUOTE_ALL)
    try:
        out.writerow(data_list)
    except:
        print "Error writing to csv."


i = 0

filename = 'data/coffee_data.csv'
csv_headers = ['coffee', 'company', 'rating', 'city', 'state', 'origin', 'roast', 'description']
append_to_csv(filename, 'w', csv_headers)

#want to scrape 130 pages
while i < 130:
    url = 'http://www.coffeereview.com/reviews/page/' + str(i)
    print "Extracting Links From Page: " + str(i) + ": " + url
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content)
    links = soup.find_all('a')

    review_links = []

    for link in links:
        if 'Complete Review' in link.text:
            review_links.append(link)

    hrefs = [link['href'].strip() for link in review_links]
    raw_sessions = []

    for url in hrefs:
        souped_content = get_content_from_review_url(url)
        content = souped_content.find(id='content')
        content = content.prettify()
        raw_sessions.append(content)

    #save the data in a pkl doc for possible future analysis
    pkl_filename = 'data/coffee_data.pkl'
    with open(pkl_filename,'w') as outfile:
        pickle.dump(raw_sessions,outfile)

    with open(pkl_filename,'r') as infile:
       raw_sessions = [BeautifulSoup(page) for page in pickle.load(infile)]

    for page in raw_sessions:
        review_info = extract_info_from_review(page)
        append_to_csv(filename, 'a+', review_info)

    i += 1
