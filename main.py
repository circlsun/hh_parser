import requests
from itertools import count
from pprint import pprint
from datetime import date, timedelta


def fetch_rating_vacancies(language):
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': f'Программист {language}',
        'area': 1,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    count = response.json()['found']
    return count


def fetch_salary(language):
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': f'Программист {language}',
        'area': 1,
        'period': 30,
        'describe_arguments': True
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(vacancy):
    if vacancy is None:
        return None
    elif vacancy['currency'] != 'RUR':
        return None
    elif vacancy['from'] and vacancy['to']:
        return (vacancy['from'] + vacancy['to']) / 2
    elif vacancy['to'] and vacancy['from'] is None:
        return vacancy['to'] * 0.8
    elif vacancy['from'] and vacancy['to'] is None:
        return vacancy['from'] * 1.2


def get_average_salary(vacancy):
    total_salary = 0
    vacancies_processed = 0
    for page in range(20):
        if predict_rub_salary(vacancy[page]['salary']) is not None:
            total_salary += predict_rub_salary(vacancy[page]['salary'])
            vacancies_processed += 1
    average_salary = int(total_salary / vacancies_processed)
    return vacancies_processed, average_salary


def fetch_all_vacancies(language):
    total = []
    url = 'https://api.hh.ru/vacancies'
    for page in range(99):
        page_response = requests.get(
            url, params={
                'page': page,
                'text': f'программист {language}',
                'area': 1,
            }
        )
        page_response.raise_for_status()
        page_payload = page_response.json()

        total.append(page_payload['items'])
        if page >= page_payload['pages']:
            break
    return total



def main():
    languages = [
        'Javascript',
        'Python',
        'Go',
        'Java',
        'Kotlin',
        'PHP',
        'C#',
        'Swift',
        'R',
        'Ruby',
        'C',
        'C++',
        'Matlab',
        'TypeScript',
        'Scala'
    ]
    # language_metric = []
    # for language in languages:
    #     temporary = {}
    #     vacancy = fetch_salary(language)['items']
    #     temporary['vacancies_found'] = fetch_rating_vacancies(language)
    #     temporary['vacancies_processed'] = get_average_salary(vacancy)[0]
    #     temporary['average_salary'] = get_average_salary(vacancy)[1]
    #     language_metric.append(temporary)
    #
    # catalog_vacancies = dict(zip(languages, language_metric))
    # pprint(catalog_vacancies)

    # language_metric = []
    # all = fetch_all_vacancies('Kotlin')[17]['items'][0]['salary']
    # temporary = {}
    # vacancy = fetch_salary(languages[4])['items']
    # temporary['vacancies_found'] = fetch_rating_vacancies('Kotlin')
    # temporary['vacancies_processed'] = get_average_salary(vacancy)[0]
    # temporary['average_salary'] = get_average_salary(vacancy)[1]
    # language_metric.append(temporary)


    language_metric = []
    for language in languages:
        try:
            # плохое название, но без конкретики лучше не сделать
            all_vacancies = fetch_all_vacancies(language)
        except requests.exceptions.HTTPError as error:
            print(error)
        total_salary = 0
        vacancies_processed = 0
        alll = []
        temporary = {}
        for job in all_vacancies:
            for vacancy in job:
                if predict_rub_salary(vacancy['salary']) is not None:
                    total_salary += predict_rub_salary(vacancy['salary'])
                    vacancies_processed += 1
            average_salary = int(total_salary / vacancies_processed)
            alll.append(average_salary)
            avrg = int(sum(alll) / len(alll))

            temporary['vacancies_found'] = fetch_rating_vacancies(language)
            temporary['vacancies_processed'] = vacancies_processed
            temporary['average_salary'] = average_salary
            language_metric.append(temporary)

    catalog_vacancies = dict(zip(languages, language_metric))
    pprint(catalog_vacancies)
  



if __name__ == '__main__':
    main()
