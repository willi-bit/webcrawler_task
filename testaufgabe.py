import os
from bs4 import  BeautifulSoup
import requests
import json
import re

def run():
    #testing other url:
    # https://www.springerprofessional.de/wasserwirtschaft-2-3-2022/20179054 \ works just fine for every other Springer Professional page with the same html signature
    base_url = 'https://www.springerprofessional.de'
    html = requests.get('https://www.springerprofessional.de/wasserwirtschaft-4-2019/16592584').text
    #Also worked with the url down below
    #html = requests.get('https://www.springerprofessional.de/wasserwirtschaft-2-3-2022/20179054').text

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

    count = soup.select_one('span.tertiary').text
    count = int(re.findall(r'\d+', count)[0])
    # to initalize a list of data with the required amount
    data_list = []

    for x in range(count):
        data_list.append(data.copy())
    #in Python, lists are similar to a Pointer-Array in C, therefore a copy of the data dict is required

    links = list()

    # first number of the headline is the Ausgabe, second number is the year of release
    # The starting page title is equal to the Ausgabe, as all content listed below was published in this paper
    text = soup.select_one('h1.issue-title').text
    text = re.findall(r'\d+', text)  # this finds all positive integers

    i = 0 #used
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
    for link in links: #going through each page found on the main page in order they were found, while also counting up i in order to add the content to the correct data object in the data_list
        page = BeautifulSoup(requests.get(link).text, 'html.parser')
        datum_kategorie = page.select_one('p.tag-line--default').text.strip()
        datum_kategorie_text = datum_kategorie.split('|')
        data_list[i]['Datum'] = datum_kategorie_text[0]
        data_list[i]['Kategorie'] = datum_kategorie_text[1].strip()

        autoren_text = page.find('p', class_='authors-info-display rich-text') #select_one caused a bug here, as it always returned None, but find with th exact same parameters worked
        if(autoren_text is not None): #some pages do not have listed authors
            data_list[i]['Autoren'] = re.sub("\s+", " ",autoren_text.text).replace('verfasst von: ','').strip()

        data_list[i]['URL'] = link
        data_list[i]['Titel'] = page.select_one('h1').text

        i += 1

    print(data_list)
    print('The result was also added to a JSON file called "result.json"!')

    with open('result.json', 'w') as f:
        f.write(json.dumps(data_list))
        f.close()

if __name__ == '__main__':
    run()