import re
import bs4
import json
import requests
from fake_headers import Headers

if __name__ == '__main__':

    headers = Headers(browser='chrome', os='win')
    headers_data = headers.generate()
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

    vacancy_list = {}

    for i in range(30):
        url = url + f'&page={i}'
        html = requests.get(url, headers=headers_data).text
        soup = bs4.BeautifulSoup(html, 'lxml')

        parameter = 'HH-MainContent HH-Supernova-MainContent'
        hh_tag_list = soup.find('div', class_=parameter)
        hh_tag_content = hh_tag_list.find_all('div', class_='serp-item')

        for values in hh_tag_content:
            # Описание вакансии:
            vacancy_tag = values.find('h3')
            vacancy_tag_content = vacancy_tag.find('a')
            vacancy = vacancy_tag_content.text

            if 'Django' in vacancy or 'Flask' in vacancy:
                # Ссылка на вакансию:
                link_tag = values.find('h3')
                link_tag_content = link_tag.find('a')
                link = link_tag_content['href']

                # Вилка ЗП:
                parameter = 'bloko-header-section-3'
                salary_tag = values.find('span', class_=parameter)
                if salary_tag is None:
                    salary = 'Не указана.'
                else:
                    salary = salary_tag.text.replace('\u202f', ' ')

                # Название компании:
                parameter = 'vacancy-serp-item-company'
                company_div = values.find('div', class_=parameter)
                company_tag = company_div.find('a')
                company = company_tag.text.replace('\u202f', ' ')

                # Город:
                parameter = 'vacancy-serp__vacancy-address'
                city_div = values.find(attrs={'data-qa': parameter})
                city = city_div.text
                city = re.search(r'Москва|Санкт-Петербург', city).group(0)

                id_vacancy = re.search(r'\d+', link).group(0)

                vacancy_list[id_vacancy] = {
                    'link': link,
                    'salary': salary,
                    'company': company,
                    'city': city
                }

    with open('vacancy.json', 'w', encoding='utf-8') as f:
        json.dump(vacancy_list, f, ensure_ascii=False)
