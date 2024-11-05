# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 21:41:36 2024

@author: Корнилов
"""

import json
import requests
from bs4 import BeautifulSoup
from configparser import ConfigParser


def get_page_layout(link: str) -> BeautifulSoup:
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def data_extraction(soup: BeautifulSoup, data_site: dict) -> None:
    # получение разметку в <div> из класс quote(цитаты)
    quote_elements = soup.find_all('div', class_='quote')

    # проходимся по каждой цитате с целью получения ее текста, тегов, автора
    for quote_element in quote_elements:
        text = quote_element.find('span', class_='text').text
        author = quote_element.find('small', class_='author').text
        tag_elements = quote_element.find(
            'div', class_='tags').find_all('a', class_='tag')
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        author_link = quote_element.find('a', href=True)['href']
        link_to_information_abouut_author = f'{base_link}{author_link}'
        #  проверяем, встречался ли данный автор уже
        #  если да, нам не нужно парсить информацию об авторе, дате и месте
        if author not in data_site:
            soup_page_about_authot = get_page_layout(
                link_to_information_abouut_author)
            bord_date = soup_page_about_authot.find(
                'span', class_='author-born-date').text
            author_born_location = soup_page_about_authot.find(
                'span', class_='author-born-location').text
            bord = f'{bord_date} {author_born_location}'

            description = soup_page_about_authot.find(
                'div', class_='author-description').text
            data_site[author] = {
                'Bord': bord,
                'Description': description,
                'Quotes': [
                        {
                            'text': text,
                            'tags': ', '.join(tags)
                            }
                    ]
                }
        else:
            new_quote = {
                'text': text,
                'tags': ', '.join(tags)
                }
            data_site[author]['Quotes'].append(new_quote)


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    base_link = config['link']['base_link']

    information_site = {}
    soup = get_page_layout(base_link)
    data_extraction(soup, information_site)
    next_li_element = soup.find('li', class_='next')

    #  перебирраем страницы до тех пор, пока они есть
    while next_li_element is not None:
        next_page_relative_url = next_li_element.find('a', href=True)['href']
        page = requests.get(f'{base_link}{next_page_relative_url}')
        soup = BeautifulSoup(page.text, 'html.parser')
        data_extraction(soup, information_site)
        # ищем HTML элемент на новой странице
        next_li_element = soup.find('li', class_='next')

    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(information_site, json_file, ensure_ascii=False, indent=4)
