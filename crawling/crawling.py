import requests
from bs4 import BeautifulSoup
import json

"""
    Requires:
        beautifulsoup4==4.12.2
        Requests==2.31.0

"""

def get_wikipedia_info(url, max_words=150):
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text.strip()

        ####limitacion
        paragraphs = [p.text.strip() for p in soup.find_all('p')]
        text = "\n\n".join(paragraphs)
        text_words = text.split()
        if len(text_words) > max_words:
            text = " ".join(text_words[:max_words])
        #print(text)
        page_info = {
            "id": url.split('=')[-1],
            "url": url,
            "title": title,
            "text": text
        }

        return page_info
    else:
        print(f'Error al obtener la página: {url}')
        return None


def get_wikipedia_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        wiki_links = [link for link in links if link.startswith('/wiki/')]

        ################################### aqui la base
        base_url = 'https://en.wikipedia.org'
        full_links = [base_url + link for link in wiki_links]

        # print(full_links)
        return full_links
    else:
        print(f'Error al obtener la página: {url}')
        return []

#Extraccion
def recursive_extraction(start_url, depth):
    # print(start_url)
    if depth <= 0:
        return []

    page_info = get_wikipedia_info(start_url)
    if page_info is None:
        return []
    # print(page_info)
    links = get_wikipedia_links(start_url)
    sub_links = []

    for link in links:
        sub_links.extend(recursive_extraction(link, depth - 1))

    return [page_info] + sub_links


start_url = 'https://en.wikipedia.org/wiki?curid=54287928'

max_depth = 4

result = recursive_extraction(start_url, max_depth)

with open('output.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print('Si se pudo jefe!!')