from numpy import single
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from locale import LC_TIME, setlocale
import pytz

setlocale(LC_TIME, 'de_DE')

# from ..models import Event 

# scraper looks at orchestra and chamber music events 


# goes to details page of given concert and returns composers : pieces as dict 
def get_concert_details(details_link):
    data = requests.get(details_link)
    soup = BeautifulSoup(data.text, 'html.parser')
    
    # lists every composer , piece as tuple (excludes empty divs)
    
    pieces = []
    for item in soup.find_all('div' , {'class' : 'piece'}):
        piece_list = []
        for piece in item.find_all('p' , {'class' : 'light'}):
            piece_list.append(piece.get_text(strip=True))
        pieces.append(piece_list)
            
    print(pieces)

    pieces_dict = {}
    # adds composers and pieces to dict, if composer already has an entry only the piece will be added
    for piece in pieces: 
        if piece[0] not in pieces_dict:
            pieces_dict[piece[0]] = [piece[1]]
        else:
            pieces_dict[piece[0]].append(piece[1])

    return pieces_dict

def date_march(concert_date):

    if concert_date.split(' ')[1] != 'Mär':
        concert_date = datetime.strptime(concert_date, '%d. %b %Y,  %H.%M')
    else:
        concert_date = concert_date.split(' ')
        concert_date[1] = 'Mrz'
        concert_date = ' '.join(concert_date)
        concert_date = datetime.strptime(concert_date, '%d. %b %Y,  %H.%M')
    return pytz.timezone('Europe/Berlin').localize(concert_date).strftime('%m.%d.%Y %H:%M')
    



def main():
    concerts = []
    month_list = ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07']
    # month_list = ['2023-01']



    for month in month_list:
        print(month, '\n')
        urls = [('https://www.berliner-philharmoniker.de/konzerte/kalender/veranstaltungen/von/' + month + '/cat/orchestra/', 'orchestra')]

        for url in urls:
            data = requests.get(url[0])

            soup = BeautifulSoup(data.text, 'html.parser')

            # find each concert in concert list 
            for element in soup.find_all('article', { 'class' : 'calendar-entry ' + url[1]}):

                singleevent = {}

                singleevent['ensemble'] = 'Berliner Philharmoniker'

                # if urls.index(url) == 0:
                #     singleevent['ensemble'] = 'Kammermusik'
                #     singleevent['type'] = 'Kammermusik'
                # else:
                #     singleevent['ensemble'] = 'Berliner Philharmoniker'


                # get details from each concert 
                concert_date = element.find('p', {'class' : 'date-and-time'})

                musicians = element.find_all(['h2', 'h3'], {'class' : ['main-musician', 'other-musician']})


                # create datetime objects from concert_date - sample: Samstag,08. Jan 2022, 19.00 Uhr
                concert_date = ' '.join(concert_date.text.split(' ')[:-1])

                # convert Mär to Mrz so strptime can parse data for march
                concert_date = date_march(concert_date)

                singleevent['datetime'] = concert_date


                # get musicians / orchester from musicians element 
                singleevent['musicians'] = {}
                singleevent['conductor'] = ''  
                for div in musicians:
                    musician = div.contents[0].get_text(strip=True)
                    role = div.find('span', {'class' : 'role'})

                    if not role:
                        if musician == 'Berliner Philharmoniker':
                            continue
                        singleevent['musicians'][musician] = ''
                    else:
                        if not role.contents:
                            singleevent['musicians'][musician] = ''
                            continue
                        if role.contents[0] == ' Dirigent ' or role.contents[0] == ' Dirigentin ':
                            singleevent['conductor'] = musician
                            continue
                        singleevent['musicians'][musician] = role.contents[0]


                # create link that leads to specific concert 
                details_link = element.find('a', {'class' : 'button grey'}, href = True)
                details_link = 'https://www.berliner-philharmoniker.de/' + details_link['href']

                # save link to singleevent 
                singleevent['link'] = details_link

                # get concert title 

                details = requests.get(details_link)
                details_soup = BeautifulSoup(details.text, 'html.parser')

                title = ''  
                if details_soup.find('h1' , {'class' : 'concert-title'}):
                    title = details_soup.find('h1' , {'class' : 'concert-title'})
                    title = title.get_text(strip=True)
                
                singleevent['title'] = title 


                # get composers, pieces and title from details_link

                data = requests.get(details_link)
                soup = BeautifulSoup(data.text, 'html.parser')
                
                # lists every composer , piece as tuple (excludes empty divs)
                
                pieces = []
                composers = []

                for item in soup.find_all('div' , {'class' : 'piece'}):
                    composers.append(item.contents[1].get_text(strip = True))

                    piece_list = []
                    for piece in item.find_all('p' , {'class' : 'light'}):
                        piece_list.append(piece.get_text(strip=True))
                    pieces.append(piece_list)
                        
                singleevent['composers'] = composers
                singleevent['pieces'] = pieces 

                # define the city of the events 
                singleevent['city'] = 'Berlin'
                # print(singleevent)

                # create entries in database for scraped data 
                # Event.objects.create(
                #     date = singleevent['date'], 
                #     city = singleevent['city'], 
                #     ensemble = singleevent['ensemble'], 
                #     musicians = singleevent['musicians'], 
                #     conductor = singleevent['conductor'],
                #     composers = singleevent['composers'],
                #     pieces = singleevent['pieces'],
                #     link = singleevent['link'])

                concerts.append(singleevent)
                # print(singleevent, '\n')

    return(concerts)

        
        

if __name__ == '__main__':
    main()