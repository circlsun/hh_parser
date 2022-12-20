import requests
from pprint import pprint


def fetch_rating_vacancies(language):
    url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': f'Программист {language}',
        'area': 1
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    count = response.json()['found']
    if count >= 100:
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
    for i in range(20):
        if predict_rub_salary(vacancy[i]['salary']) is not None:
            total_salary += predict_rub_salary(vacancy[i]['salary'])
            vacancies_processed += 1
    average_salary = int(total_salary / vacancies_processed)
    return vacancies_processed, average_salary


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
        'C/C++',
        'Matlab',
        'TypeScript',
        'Scala'
    ]
    language_metric = []
    for language in languages:
        temporary = {}
        vacancy = fetch_salary(language)['items']
        temporary['vacancies_found'] = fetch_rating_vacancies(language)
        temporary['vacancies_processed'] = get_average_salary(vacancy)[0]
        temporary['average_salary'] = get_average_salary(vacancy)[1]
        language_metric.append(temporary)

    catalog_vacancies = dict(zip(languages, language_metric))
    pprint(catalog_vacancies)


if __name__ == '__main__':
    main()
