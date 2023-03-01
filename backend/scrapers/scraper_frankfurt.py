from numpy import single
import requests
from bs4 import BeautifulSoup
from datetime import datetime 
# from ..models import Event
import pytz
from locale import setlocale, LC_TIME

setlocale(LC_TIME, 'de_DE')


def main():
    concerts = []
    # get main link for symphonic concerts 
    urls = ['https://www.hr-sinfonieorchester.de/konzerte/konzerte-22-23/konzertreihen/hr-sinfoniekonzert-110.html',
            'https://www.hr-sinfonieorchester.de/konzerte/konzerte-22-23/konzertreihen/auftakt-130.html']
    
    for url in urls:
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')

        defaultyear = '2023'

        for item in soup.find_all('li', {'style' : 'margin-top: 20px;'}):
            singleevent = {}

            # get event title 
            title = item.find('span', {'class' : 'c-eventTeaser__headline text__headline'}).text
            singleevent['title'] = title 

            day = item.find('span', {'class' : 'c-eventTeaser__day'}).text
            month = item.find('span', {'class' : 'c-eventTeaser__month'}).text
            if month == 'Sep' or month == 'Okt' or month == 'Nov' or month == 'Dez':
                year = '2022'
            else : 
                year = '2023'

            if month == 'Mär':
                month = 'Mrz'

            time = item.find('span', {'class' : 'c-eventTeaser__startTime'}).text.replace('Uhr', '')
            concert_date = day + ' ' + month + ' ' + year + ' ' + time 
            # create datetime object 
            concert_date = datetime.strptime(concert_date, '%d %b %Y %H:%M ')

            # add date to singleevent 
            singleevent['datetime'] = concert_date.strftime("%Y-%m-%dT%H:%M:%S")

            # set city to Frankfurt and Ensemble to hr-Sinphonieorchester
            singleevent['city'] = 'Frankfurt' 
            singleevent['ensemble'] = 'hr-Sinfonieorchester'

            # get musicians and conductor
            singleevent['musicians'] = {}
            singleevent['conductor'] = ''
            
            musicians = item.find_all('ul' , {'class' : 'c-concert-info__list'})[0]
            musicians = musicians.find_all('li' , {'class' : 'c-concert-info__item'})
            musicians = [musician.get_text(strip = True).split('|') for musician in musicians]

            for musician in musicians: 
                if len(musician) == 2:
                    if musician[1] in ['Dirigent', 'Dirigentin']:
                        singleevent['conductor'] = musician[0]
                        continue
                    singleevent['musicians'][musician[0]] = musician[1]
                else:
                    singleevent['musicians'][musician[0]] = ''

            # add composers and pieces 
            composers_pieces = item.find_all('ul' , {'class' : 'c-concert-info__list'})[1]
            composers_pieces = composers_pieces.find_all('li' , {'class' : 'c-concert-info__item'})
            composers = [composer.get_text(strip = True).split('|')[0] for composer in composers_pieces]
            pieces = [[piece.get_text(strip = True).split('|')[1]] if len(piece.get_text(strip = True).split('|')) > 1 else [''] for piece in composers_pieces ]
            
            singleevent['composers'] = composers
            singleevent['pieces'] = pieces 

            # add link to singleevent 
            link = item.find('a', {'class' : 'link c-teaser__headlineLink'}, href = True)
            link = link['href']
            singleevent['link'] = link 

            print(singleevent)
            
            # Event.objects.create(
            #             date = singleevent['datetime'], 
            #             city = singleevent['city'], 
            #             ensemble = singleevent['ensemble'], 
            #             musicians = singleevent['musicians'], 
            #             conductor = singleevent['conductor'],
            #             composers = singleevent['composers'],
            #             pieces = singleevent['pieces'],
            #             link = singleevent['link'])

            concerts.append(singleevent)
    return(concerts)



if __name__ == '__main__':
    main()