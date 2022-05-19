import os
from bs4 import  BeautifulSoup
import requests
import json
import re

def run():
    base_url = 'https://www.springerprofessional.de'
    html = requests.get('https://www.springerprofessional.de/wasserwirtschaft-4-2019/16592584').text
    #Creating the soup with the plain html
    soup = BeautifulSoup(html, 'html.parser')



    #A dict with all required types:
    data = {
            'Ausgabe':'',
            'Datum':'',
            'Jahr':'',
            'Kategorie':'',
            'Titel':'',
            'Autoren':'',
            'URL':''
            }

    #The starting page title is equal to the Ausgabe, as all content listed below was published in this paper
    text = soup.select_one('h1.issue-title').text
    text = re.findall(r'\d+', text)#this finds all positive integers

    count = soup.select_one('span.tertiary').text
    count = int(re.findall(r'\d+', count)[0])
    # to initalize a list of data with the required amount
    data_list = []
    for x in range(count):
        data_list.append(data)
    #first number of the headline is the Ausgabe, second number is the year of release
    #ausgabe.append(text[0])
    #jahr.append(text[1])

    links = list()

    i = 0
    #Searching for all hrefs under the "Inhaltsverzeichnis" sections, adding the base-url if the html doc uses relative links
    for section in soup.find_all('section', class_='teaser cf'):
        data_list[i]['Ausgabe'] = text[0]
        data_list[i]['Jahr'] = text[1]

        #Putting it in here, as every section was published in the same paper with the same years etc.
        link = section.find('a').get("href")
        if base_url in link:
            links.append(link)
        else:
            links.append(base_url + link)
        i += 1

    i = 0
    for link in links: #going through each page found on the main page in order they were found
        print(i)
        page = BeautifulSoup(requests.get(link).text, 'html.parser')
        datum_kategorie = page.select_one('p.tag-line--default').text.strip()
        dat_kag_text = datum_kategorie.split('|')
        data_list[i]['Datum'] = dat_kag_text[0]
        data_list[i]['Kategorie'] = dat_kag_text[1].strip()

        autoren_text = page.find('p', class_='authors-info-display rich-text') #select_one caused a bug here, as it always returned None, but find with th exact same parameters worked
        if(autoren_text is not None): #some pages do not have listed authors
            data_list[i]['Autoren'] = re.sub("\s+", " ",autoren_text.text).replace('verfasst von: ','').strip()
        else:
            data_list[i]['Autoren'] = ''
        data_list[i]['URL'] = link
        data_list[i]['Titel'] = page.select_one('h1').text
        print(data_list)
        i += 1
    print(data_list)
if __name__ == '__main__':
    run()