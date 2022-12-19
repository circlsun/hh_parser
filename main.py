import requests
from pprint import pprint


def fetch_hh_vacancies():
    base_url = 'https://api.hh.ru/vacancies'
    response = requests.get(base_url)
    response.raise_for_status()
    pprint(response.json())


def main():
    fetch_hh_vacancies()


if __name__ == '__main__':
    main()
