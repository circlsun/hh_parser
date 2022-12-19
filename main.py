import requests
from pprint import pprint


def fetch_hh_vacancies(period=None):
    base_url = 'https://api.hh.ru/vacancies'
    payload = {
        'text': 'программист',
        'area': 1,
        'period': period
    }
    response = requests.get(base_url, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    print(fetch_hh_vacancies()['found'] - fetch_hh_vacancies(period=30)['found'])


if __name__ == '__main__':
    main()
