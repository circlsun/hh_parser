import requests
import json
from pprint import pprint

lenguages = (
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
)


def fetch_hh_vacancies(period=None):
    rating = {}
    base_url = 'https://api.hh.ru/vacancies'
    for language in lenguages:

        payload = {
            'text': f'Программист {language}',
            'area': 1,
            'period': period
        }
        response = requests.get(base_url, params=payload)
        response.raise_for_status()
        count = response.json()['found']
        if count >= 100:
            rating[language] = count
    return dict(sorted(rating.items(), key=lambda x: x[1], reverse=True))


def fetch_salary():
    salaries = {}
    base_url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': 'Программист Python',
        'area': 1
    }
    response = requests.get(base_url, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    print(json.dumps(fetch_hh_vacancies(period=30), indent=4))


if __name__ == '__main__':
    main()
