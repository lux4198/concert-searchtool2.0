import json
from numpy import single
import requests
from bs4 import BeautifulSoup
from datetime import datetime 


def main():
    concerts = []
    # download website data from main link 
    data = requests.get('https://www.staatskapelle-dresden.de/konzerte/konzertkalender/')
    # parse data into Beautifulsoup
    soup = BeautifulSoup(data.text, 'html.parser')

    # from parsed data, extract each concert item
    for item in soup.find_all('div', {'class' : 'spielplan-item'}):

        # remove concert items that take place in chamber music hall (Semper Zwei)
        if item.find('div', {'class' : 'zeit'}).contents[1].text == 'Semper Zwei':
            continue
        

        # singleevent variable stores info about concert item before passing it to Event model 
        singleevent = {}

        # get the link to concert details from item 
        link = item.find('a', href=True)
        link = 'https://www.staatskapelle-dresden.de/' + link['href']
        singleevent['link'] = link

        # get json data from script tag of each concert item
        json_data = item.find('script', {'type' : 'application/ld+json'}).get_text()
        json_data = json.loads(json_data)


        # extract concert Datetime
        concert_date = json_data['startDate']
        # create datetime object 
        concert_date = datetime.strptime(concert_date, '%Y-%m-%dT%H:%M')
        # add date to singleevent 
        singleevent['datetime'] = concert_date.strftime("%Y-%m-%dT%H:%M:%S")


        # add city to singleevent 
        # if orchestra plays at another city, check for 'Gastconcert' in title and extract city
        if 'Gastkonzert in' in json_data['name']:
            city = json_data['name'].split(' ')[2]
        else:
            city = 'Dresden'
        singleevent['city'] = city 
        

        # default ensemble is Staatskapelle Dresden
        singleevent['ensemble'] = 'Staatskapelle Dresden'

        # get title
        singleevent['title'] = item.find('strong', {'class' : 'name'}).text

        # go to concert details page and parse data
        details = requests.get(singleevent['link'])
        concert_details = BeautifulSoup(details.text, 'html.parser')

        
        # extract musicians and conductor from details page 
        singleevent['musicians'] = {}
        singleevent['conductor'] = ''

        if concert_details.find('div', {'class' : 'mitwirkende'}):
            # each musician has a div within 'mitwirkende'
            musicians = concert_details.find('div', {'class' : 'mitwirkende'}).find_all('div')

            # each musician div contains the name and role of musician (usually)
            for musician in musicians:
                player = musician.contents[0].get_text(strip = True)
                role = musician.contents[1].get_text(strip = True)

                # add conductor to singleevent
                if role in ['Dirigent', 'Dirigentin']:
                    singleevent['conductor'] = player 
                    continue
        
                # add musician and role to musicians dict
                singleevent['musicians'][player] = role

        # extract composers and pieces from div 'Werke'
        singleevent['composers'] = ''
        singleevent['pieces'] = ''
        if concert_details.find('div', {'class' : 'werke'}) and not concert_details.find('div', {'class' : 'werke'}).text == '':

            composers_pieces = concert_details.find('div', {'class' : 'werke'})

            # get composers from h3 tags (composer highlighted in div)
            composers = [composer.get_text(strip = True) for composer in composers_pieces.find_all('h3')]

            # get pieces from li tags within each ul element
            # ul element contains all pieces of highlighted composer 
            ul_element = composers_pieces.find_all('ul')
            # lc extracts text for each li tag (so 1 piece) for each ul element (for 1 composer)
            pieces = [[li.get_text(strip = True) for li in ul] for ul in ul_element]

            singleevent['composers'] = composers 
            singleevent['pieces'] = pieces     

        else:
            continue

        # Event.objects.create(
        #     date = singleevent['datetime'], 
        #     city = singleevent['city'], 
        #     ensemble = singleevent['ensemble'], 
        #     musicians = singleevent['musicians'], 
        #     conductor = singleevent['conductor'],
        #     composers = singleevent['composers'],
        #     pieces = singleevent['pieces'],
        #     link = singleevent['link'])
        
        print(singleevent)   
        concerts.append(singleevent)
    return(concerts)

if __name__ == '__main__':
    main()