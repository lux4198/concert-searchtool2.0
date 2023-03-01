import requests
from bs4 import BeautifulSoup

def main():
    concerts = []
    for i in range(100):
        if i == 0:
            data_general = requests.get('https://www.elbphilharmonie.de/de/programm/EPHH/OR/')
        else:
            event_list = soup_general.find('ul', {'id' : 'event-list'})
            if event_list:
                link = event_list.find_all('li')[-1]
                link = 'https://www.elbphilharmonie.de/' + link['data-url']
                data_general = requests.get(link)
                print(link)
            else:
                break

        soup_general = BeautifulSoup(data_general.text, 'html.parser')

        for event in soup_general.find_all('li', {'class' : 'event-item'}):

            singleevent = {}

            # define city of Events 
            singleevent['city'] = 'Hamburg'

            # get link to each specific concert for details 
            concert_link = event.find('a', href = True)
            concert_link = 'https://www.elbphilharmonie.de/' + concert_link['href']
            singleevent['link'] = concert_link
            
            # get data from details link 
            data_details = requests.get(concert_link)
            soup_detail = BeautifulSoup(data_details.text, 'html.parser')

            # get datetime of concert from header
            date = soup_detail.find('time')['datetime']
            singleevent['datetime'] = date

            # get concert title 
            title = soup_detail.find('h1', {'class' : 'event-title no-line'})
            singleevent['title'] = title.get_text(strip=True)

            # get musicians and roles 
            singleevent['musicians'] = {}
            singleevent['conductor'] = ''

            musicians = soup_detail.find_all('p', {'class' : 'artists without-space'})
            
            if musicians:
                singleevent['ensemble'] = [musician.find('b').text for musician in musicians][0]
                for musician in musicians:
                    # musician / conductor always highlighted in bold text
                    Musician = musician.find('b').text
                    if Musician == singleevent['ensemble']:
                        continue

                    # other text in div is musicians role 
                    for role in musician.contents:
                        if role.text != Musician: 
                            Role = role.get_text(strip = True)
                    # add musicians + role to each event + add conductor as special key 
                    if Role in ['Dirigent', 'Dirigentin']:
                        singleevent['conductor'] = Musician
                        continue

                    singleevent['musicians'][Musician] = Role

            # get Pieces and Composers 
            # finds the div that contains this concerts program 
            for div in soup_detail.find_all('div', {'class' : 'cell medium-6'})[:3]:
                content = [content.get_text(strip = True) for content in div.contents if content.get_text(strip = True) != '']
                if content[0] != 'Programm':
                    continue
                else:
                    composers_pieces = div

            # gets the paragraphs with each composer + pieces from above mentioned div
            paragraphs = [paragraphs for paragraphs in composers_pieces.find_all('p')]
            
            # long list comprehension -> checks every paragraph in composers_pieces div -> extracts the text and strips it of line breaks etc
            # -> does not accept empty strings or -pause-, if paragraph does not contain program, but e.g. 'Einfuehrung', it is not accepted
            composers_and_pieces = []
            singlepiece = []
            for paragraph in paragraphs:
                if len(paragraph.contents) >= 2 and paragraph.contents[1].get_text(strip = True) != 'Einführung':
                    ls = [piece.get_text(strip = True) for piece in paragraph.contents if piece.get_text(strip = True) != '' and piece.get_text(strip = True) != '- Pause -']
                    composers_and_pieces.append(ls)
                elif len(paragraph.contents) < 2 and paragraph.contents[0].get_text(strip = True) != 'Einführung':
                    singlepiece.append(paragraph.get_text(strip = True))
                else:
                    continue

            # extracts composers and pieces from the program 
            composers = [composers[0] for composers in composers_and_pieces if composers]
            pieces = [pieces[1:] for pieces in composers_and_pieces if pieces]

            singleevent['composers'] = composers
            singleevent['pieces'] = pieces 

            # if no composer is mentioned, all of the text is put into the pieces list (e.g. for piano recitals)
            if singlepiece:
                singleevent['composers'].append(singlepiece)
                singleevent['pieces'].append([])
            
            print(singleevent, '\n')

            concerts.append(singleevent)
    return(concerts)

if __name__ == '__main__':
    main()