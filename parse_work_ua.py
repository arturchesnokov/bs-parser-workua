import logging

from helpers import *
from helpers_db import save_to_db


def main():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('parser')

    page = 0

    while True:
        page += 1

        # # TODO remove page limiter
        # if page == 5:
        #     break

        payload = {
            'ss': 1,
            'page': page,
        }

        headers = user_agent_generator()

        log.info(f'PAGE: {page}')
        response = requests.get(HOST + ROOT_PATH, params=payload, headers=headers)
        random_sleep()

        assert response.status_code == 200

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        cards = soup.select(JOB_CARD_CSS_SELECTOR)
        log.debug(f'Cards: {len(cards)}')

        # result = []

        if not cards:
            log.warning('No cards in response! -> BREAK')
            break

        # Collecting information from the vacancy:
        for card in cards:
            # General information about the vacancy:
            tag_a = card.find('h2').find('a')
            title = tag_a.text
            href = tag_a['href']

            log.debug(f'title:{title}')
            log.debug(f'href:{href}')
            log.info(f'HOST+href:{HOST + href}')

            salary = get_salary(card)
            log.debug(f'Salary:{salary}')

            company_name = get_company_name(card)
            log.debug(f'Company name:{company_name}')

            random_sleep()
            # Additional information about the vacancy from additional request:
            additional_vacancy_info = get_additional_vacancy_info(href)

            company_address = get_company_address(additional_vacancy_info)
            log.debug(f'Company address:{company_address}')

            requirements = get_requirements(additional_vacancy_info)
            log.debug(f'Requirements:{requirements}')

            description = get_description(additional_vacancy_info)
            log.debug(f'description:{description}')

            # # Collecting the results:
            # result.append([f'Position: {title}, '
            #                f'Link_id: {href}, '
            #                f'Salary: {salary}, '
            #                f'Company: {company_name}, '
            #                f'Address: {company_address}, '
            #                f'Requirements: {requirements},'
            #                f'Description: \n{description}'
            #                ]
            #               )

            save_to_db(title, href, salary, company_name, company_address, requirements, description)

            data_json = {
                'title': title,
                'link': href,
                'salary': salary,
                'company': company_name,
                'address': company_address,
                'requirements': requirements,
                'description': description
            }
            save_fo_json(data_json)

        # save_info(result)


if __name__ == '__main__':
    main()
