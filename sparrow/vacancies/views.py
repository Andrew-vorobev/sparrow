import datetime
import requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from .models import *


links = [
    {
        'title': 'Главная',
        'name': 'home',
    },
    {
        'title': 'Востребованность',
        'name': 'demand',
    },
    {
        'title': 'География',
        'name': 'geography',
    },
    {
        'title': 'Навыки',
        'name': 'skills',
    },
    {
        'title': 'Последние вакансии',
        'name': 'vacancies',
    }
]


class HH:
    def __init__(self, items):
        self.items = items

    class HHVacancy:
        def __init__(self, name, description, skills_, employer, area, salary, published_at):
            self.name = name
            self.description = description
            self.skills = skills_
            self.employer = employer
            self.area = area
            self.salary = salary
            self.published_at = published_at

    def make_vacancy(self):
        list_of_vacancies = []
        for item in self.items:
            # if 'id' in item:
                # print(item['id'])
                # break
            resp = requests.get(f'https://api.hh.ru/vacancies/{item["id"]}').json()
            if len(resp['key_skills']) == 0:
                skills_ = 'Не указаны'
            else:
                skills_ = '<ol>'
                skills_ += ''.join(map(lambda skill: '<li>' + skill['name'] + '</li>', resp['key_skills']))
                skills_ += '</ol>'
            if not resp['salary']:
                salary = 'Не указана'
            else:
                if resp['salary']['from'] and resp['salary']['to']:
                    salary = (resp['salary']['from'] + resp['salary']['to']) / 2
                elif resp['salary']['from'] and not resp['salary']['to']:
                    salary = resp['salary']['from']
                elif not resp['salary']['from'] and resp['salary']['to']:
                    salary = resp['salary']['to']
                else:
                    salary = 'Не указана'
            date = '{0[2]}.{0[1]}.{0[0]}'.format(resp['published_at'][:10].split('-'))
            list_of_vacancies.append(self.HHVacancy(resp['name'], resp['description'], skills_, resp['employer']['name'], resp['area']['name'], salary, date))
        return list_of_vacancies


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/home.html', {
        'title': links[0]['title'],
        'links': links,
    })


def demand(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/demand.html', {
        'title': links[1]['title'],
        'links': links,
        'stats': Stats.objects.all(),
        'images': Image.objects.all(),
        'types': Type.objects.all(),
    })


def geography(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/geography.html', {
        'title': links[2]['title'],
        'links': links,
        # 'stats': Stats.objects.all(),
        # 'images': Image.objects.all(),
        'types': Type.objects.all(),
    })


def skills(request: HttpRequest) -> HttpResponse:
    return render(request, 'vacancies/skills.html', {
        'title': links[3]['title'],
        'links': links,
        # 'stats': Stats.objects.all(),
        # 'images': Image.objects.all(),
        'types': Type.objects.all(),
    })


def vacancies(request: HttpRequest) -> HttpResponse:
    response = requests.get('https://api.hh.ru/vacancies?specialization=1&per_page=10&page=1&date_from=2022-12-14T00:00:00&date_to=2022-12-14T23:59:59&text=NAME:(frontend)')
    json = response.json()['items']
    # print(json)
    hh = HH(json)
    # return HttpResponse(dir(response))
    # print(len(response.json()['items']))
    # return HttpResponse(response['items'])
    return render(request, 'vacancies/vacancies.html', {
        'title': links[4]['title'],
        'links': links,
        'items': hh.make_vacancy()
    })
