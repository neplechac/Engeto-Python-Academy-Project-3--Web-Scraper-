import csv
import requests as rq
from bs4 import BeautifulSoup as bs
from unicodedata import normalize

DEF_URL = 'https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ'
BASE_URL = 'https://volby.cz/pls/ps2017nss/'

def selection(num): # supporting function for select_district() & input validity checker
    while True:
        try:
            selection = int(input('Please select a number: '))
            if not selection in range(1,num):
                print('Invalid selection. Your number is out of range.')
            else:
                break
        except ValueError:
            print('Invalid selection. You have not entered a valid number.')
    return selection

def select_district(): # select region and district & return its url

    # SELECT REGION
    print('-'*30)
    regions = {}
    reg_num = 1
    for h3 in main_soup.find_all('h3', {'class':'kraj'}):
        regions[h3.a.text.strip()] = reg_num
        reg_num += 1
    for r,n in regions.items():
        print(n,r)
    print('-'*30)

    reg_num = selection(reg_num)

    # SELECT DISTRICT
    print('-'*30)
    districts = {}
    dist_num = 1
    for td in main_soup.find_all('td', {'headers':'t{0}sa1 t{0}sb2'.format(str(reg_num))}):
        districts[td.text.strip()] = dist_num
        dist_num += 1
    for d,n in districts.items():
        print(n,d)
    print('-'*30)

    dist_num = selection(dist_num)

    # :)
    if reg_num == 2 and dist_num == 13:
        print('Sorry, this script is too simple to process votes from abroad.:(')
        quit()

    # get district URL
    for td in main_soup.find_all('td', {'headers':'t{}sa3'.format(str(reg_num))}):
        dist_url = td.a['href']
        if dist_url[-1] == str(dist_num):
            break
    return dist_url

def csv_filename(): # set csv filename and check, if it is valid
    print('-'*30)
    csv_name = input('Please enter name of the csv file: ')

    # FILENAME CHECKER
    while True:
        if csv_name == '' or csv_name == ' '*len(csv_name):
            print('Invalid filename.')
            print('You cannot use empty name.')
            csv_name = input('Please enter name of the csv file: ')
        elif any((ch in '\\/?%*:|".<>') for ch in csv_name):
            print('Invalid filename.')
            print('You cannot use any of the following characters: \\/?%* :|".<>')
            csv_name = input('Please enter name of the csv file: ')
        else:
            break
    return csv_name

def get_municipalities(): # get id and name of every municipality
    municipalities = []
    for tr in dist_soup.find_all('tr'):
        municipality = []
        for td in tr.find_all('td'):
            if td.text != 'X' and td.text != '-':
                municipality.append(td.text.strip())
        if municipality != []:
            municipalities.append(municipality)
    return municipalities

def load_overall(overall_table): # first half of get_results()
    overall = []
    for td in overall_table.find_all('td', {'class':'cislo'}):
        overall.append(normalize('NFKC', td.text.strip()))
    return overall

def load_parties(parties_table, i): # second half of get_results()
    parties = []
    for tr in parties_table[i].find_all('tr'):
        party = []
        for td in tr.find_all('td'):
            if td.text != 'X' and td.text != '-':
                party.append(normalize('NFKC', td.text.strip()))
        if party != []:
            parties.append(party)
    return parties

def get_results(): # get data for every municipality
    results = []
    for td in dist_soup.find_all('td', {'class':'cislo'}):
        muni_page = rq.get(BASE_URL + td.a['href'])
        muni_soup = bs(muni_page.text, 'html.parser')

        overall_table = muni_soup.find('table', {'id': 'ps311_t1'})
        parties_table = muni_soup.find_all('div', {'class':'t2_470'})

        overall_results = load_overall(overall_table)
        parties_results = load_parties(parties_table, 0) + load_parties(parties_table, 1)
        municipality_results = overall_results + parties_results

        results.append(municipality_results)
    return results

def create_csv(muni_list, resu_list, csv_name):
    final_list = list(zip(muni_list, resu_list))

    with open('{}.csv'.format(csv_name),'w') as file:
        writer = csv.writer(file)

        # HEADER
        header = ['code', 'location', 'registered', 'envelopes', 'valid']
        for i in range(9,len(resu_list[0])):
            header.append(resu_list[0][i][1])
        writer.writerow(header)

        # DATA
        for item in final_list:
            location = item[0][0], item[0][1],
            numbers = item[1][3], item[1][4], item[1][7],
            for i in range(9,len(item[1])):
                numbers += item[1][i][2],
            writer.writerow(location + numbers)

        print('CSV has been created.')

if __name__ == '__main__':
    print('-'*30)

    # 1) Check connection & get main page
    try:
        main_page = rq.get(DEF_URL)
        main_soup = bs(main_page.text, 'html.parser')
    except:
        print('Could not get the page. Please try again.')
        quit()
    else:
        print('Connection OK')

    # 2) Select district & choose filename
    URL = BASE_URL + select_district()
    csv_name = csv_filename()

    # 3) Get all the data
    print('-'*30)
    print('Processing...')
    dist_page = rq.get(URL)
    dist_soup = bs(dist_page.text, 'html.parser')

    muni_list = get_municipalities()
    resu_list = get_results()

    # 4) Create file & write data into it
    create_csv(muni_list, resu_list, csv_name)

    # create_csv() HELP:

    # muni_list[x][y]:
    # x - municipality
    # y=0/1 - id/name

    # resu_list[x][y][z]:
    # x - municipality
    # y=0-8 - overall dist.no./dist.processed/dist.percentage/registered/enevelopes/turnout/casted/valid/percent.valid
    # y=9+ - party
    # z=0/1/2/3 - party no./name/votes/percentage
