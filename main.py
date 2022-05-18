import os
from bs4 import  BeautifulSoup
import requests
import csv
import webbrowser
""""
def create_project_dir(directory):
    if not os.path.exists(directory):
        print(f'Creating directory: {directory}')
        os.makedirs(directory)

def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

#Add content to existing file
def append_to_file(path, data):
    with open(path, 'a', encoding="utf-8") as file:
        file.write(data + '\n')

def delete_file_content(path):
    with open(path, 'w'):
        pass

def file_to_set(file_name):
    results = set()
    with open(file_name,'rt') as f:
        for line in f:
            results.add(line.strip()) #maybe i have to replace with .replace('\n', '')
    return results

def set_to_file(path, data):
    delete_file_content(path)
    for link in sorted(data):
        append_to_file(path, link)
"""""
def run():
    base_url = 'https://www.springerprofessional.de'
    html = requests.get('https://www.springerprofessional.de/wasserwirtschaft-4-2019/16592584').text
    #Creating the soup with the plain html
    soup = BeautifulSoup(html, 'html.parser')

    links = set()

    #JSON dataset:
    ausgabe, datum, jahr, kategorie, titel, autoren, url = []
    data_set = {'Ausgabe':ausgabe,'Datum':datum,'Jahr':jahr,'Kategorie':kategorie,'Titel':titel,'Autoren':autoren,'URL':url}


    #Searching for all hrefs under the "Inhaltsverzeichnis" sections, adding the b
    for section in soup.find_all('section', class_='teaser cf'):
        link = section.find('a').get("href")
        if base_url in link:
            links.add(link)
        else:
            links.add(base_url + link)

    #Creating queue, remaining pages that have to be scraped
    #Maybe copying it into a file, would be more readable: set_to_file('springer/queue.txt', links)
    for link in sorted(links): #sorted by alphabetic order
        page = BeautifulSoup(requests.get(link).text, 'html.parser')
        page.select('h1').text

if __name__ == '__main__':
    run()