import random
from time import sleep
from user_agent import generate_user_agent
import requests
from bs4 import BeautifulSoup
import json

HOST = 'https://www.work.ua'
ROOT_PATH = '/ru/jobs/'

# css celector -> <div class ="card card-hover card-visited wordwrap job-link">
JOB_CARD_CSS_SELECTOR = 'div.card.card-hover.card-visited.wordwrap.job-link'


def save_info(array: list) -> None:
    with open('work-ua.txt', 'a') as file:
        for line in array:
            file.write(' | '.join(line) + '\n')


def random_sleep():
    sleep(random.randint(1, 3))


def user_agent_generator():
    user_agent = generate_user_agent()
    headers = {
        'User-Agent': user_agent,
    }
    return headers


def save_fo_json(data: dict) -> None:
    with open('work-ua.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.write('\n')


def get_salary(card):
    try:
        salary = card.find('div', class_='').find('b').text
    except AttributeError:
        salary = 'No information'
    return salary


def get_company_name(card):
    company_name = card.find('div', class_='add-top-xs').find('b').text
    return company_name


def get_additional_vacancy_info(href):
    headers = user_agent_generator()
    response_additional = requests.get(HOST + href, headers=headers)
    return BeautifulSoup(response_additional.text, 'html.parser')


def get_description(vacancy_info):
    try:
        # TODO avoid repeating of text if
        description_list = vacancy_info.find('div', id='job-description').find_all(['p', 'b', 'li'])
        description = ''.join(i.text + '\n' for i in description_list)
    except AttributeError:
        description = 'No information'
    return description


def get_company_address(vacancy_info):
    try:
        address_requirements = vacancy_info.select('p.text-indent.add-top-sm')
        for tag_p in address_requirements:
            if tag_p.find('span', attrs={"title": "Адрес работы"}):
                company_address = tag_p.text.strip().split('.')[0]
    except AttributeError:
        company_address = 'No information'
    return company_address


def get_requirements(vacancy_info):
    try:
        address_requirements = vacancy_info.select('p.text-indent.add-top-sm')
        for tag_p in address_requirements:
            if tag_p.find('span', attrs={"title": "Условия и требования"}):
                requirements_list = tag_p.text.strip().split('.')
                requirements = ''.join(r.strip() + '. ' for r in requirements_list)[:-3]
    except AttributeError:
        requirements = 'No information'
    return requirements
