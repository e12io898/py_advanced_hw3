import requests
import re
from fake_headers import Headers
import bs4

if __name__ == '__main__':

    headers = Headers(browser='firefox', os='win')
    headers_data = headers.generate()

    job_list = {}
    key = 1

    for i in range(1):
        url = f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={i}'
        html = requests.get(url, headers=headers_data).text
        soup = bs4.BeautifulSoup(html, 'lxml')

        hh_tag_list = soup.find('div', class_='HH-MainContent HH-Supernova-MainContent')

        hh_tag_content = hh_tag_list.find_all('div', class_='serp-item')

        for values in hh_tag_content:
            # Ссылка на вакансию:
            h3_tag = values.find('h3')
            h3_tag_content = h3_tag.find('a')
            link = h3_tag_content['href']

            # Вилка ЗП:
            span_tag = values.find('span', class_='bloko-header-section-3')
            if span_tag is None:
                salary = 'Не указана'
            else:
                salary = span_tag.text

            # Название компании:
