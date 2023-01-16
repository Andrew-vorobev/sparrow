import numpy as np
import requests
from lxml import etree
import matplotlib.pyplot as plt

import pandas as pd

# from processing.models import Valuta

currency_to_rub = {
    "AZN": 35.68, "BYR": 23.91, "EUR": 59.90, "GEL": 21.74, "KGS": 0.76,
    "KZT": 0.13, "RUR": 1, "UAH": 1.64, "USD": 60.66, "UZS": 0.0055,
}

VACANCIES_FILE = './data/vacancies_with_skills.csv'


class Demand:
    def __init__(self):
        self.df = pd.read_csv(VACANCIES_FILE, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at'])
        self.df['average'] = self.df[['salary_from', 'salary_to']].mean(axis=1)
        self.df['salary'] = self.df.apply(self.get_salary, axis=1)
        self.df['date'] = self.df.apply(self.get_date, axis=1)
        self.df['year'] = self.df.apply(self.get_year, axis=1)
        self.df.dropna(subset=['salary'], inplace=True)

        df2 = self.df[self.df['name'].str.contains('|'.join(['ERP-специалист', 'erp', 'enterprise resource planning', 'abap', 'crm', 'help desk', 'helpdesk', 'service desk', 'servicedesk', 'bi', 'sap']), case=False)]

        new_df = pd.DataFrame()

        new_df['salary'] = self.df.groupby(['year'])['salary'].mean()
        new_df['count'] = self.df.groupby(['year']).size()

        new_df['s_salary'] = df2.groupby(['year'])['salary'].mean()
        new_df['s_count'] = df2.groupby(['year']).size()
        print(new_df)
        # print(new_df.to_dict())

        stats = new_df.to_dict()

        # fig, ax = plt.subplot()

        # ax.
        # print(list(stats['salary'].values()))
        # print(list(stats['salary'].keys()))

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.bar(list(stats['salary'].keys()), list(stats['salary'].values()))
        ax.set_title('Динамика уровня зарплат по годам')
        ax.set_ylabel('Зарплата, руб.')
        ax.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        # fig.autofmt_xdate()
        fig.savefig('image_1.png')

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.bar(list(stats['count'].keys()), list(stats['count'].values()))
        ax.set_title('Динамика количества вакансий по годам')
        ax.set_ylabel('Кол-во вакансий')
        ax.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        # fig.autofmt_xdate()
        fig.savefig('image_2.png')

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.bar(list(stats['s_salary'].keys()), list(stats['s_salary'].values()))
        ax.set_title('Динамика уровня зарплат по годам для выбранной профессии')
        ax.set_ylabel('Зарплата, руб.')
        ax.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        # fig.autofmt_xdate()
        fig.savefig('image_3.png')

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.bar(list(stats['s_count'].keys()), list(stats['s_count'].values()))
        ax.set_title('Динамика количества вакансий по годам для выбранной профессии')
        ax.set_ylabel('Кол-во вакансий')
        ax.set_xlabel('Год')
        plt.xticks(rotation=90)
        plt.tight_layout()
        # fig.autofmt_xdate()
        fig.savefig('image_4.png')

        # fig, ax = plt.subplots(nrows=1, ncols=1)
        # ax.bar(list(stats['count'].keys()), list(stats['count'].values()))
        # ax.set_title('')
        # ax.set_ylabel('')
        # ax.set_xlabel('Год')
        # fig.autofmt_xdate()
        # fig.savefig('image_2.png')
        #
        # fig, ax = plt.subplots(nrows=1, ncols=1)
        # ax.bar(list(stats['s_salary'].keys()), list(stats['s_salary'].values()))
        # ax.set_title('Динамика уровня зарплат по годам для выбранной профессии')
        # ax.set_ylabel('Зарплата, руб.')
        # ax.set_xlabel('Год')
        # fig.autofmt_xdate()
        # fig.savefig('image_3.png')
        #
        # fig, ax = plt.subplots(nrows=1, ncols=1)
        # ax.bar(list(stats['s_count'].keys()), list(stats['s_count'].values()))
        # ax.set_title('Динамика количества вакансий по годам для выбранной профессии')
        # ax.set_ylabel('Кол-во вакансий')
        # ax.set_xlabel('Год')
        # fig.autofmt_xdate()
        # fig.savefig('image_4.png')



        # self.df.to_csv('data/ioutput.csv')

    @staticmethod
    def get_salary(row):
        try:
            return row['average'] * currency_to_rub[row['salary_currency']]
        except:
            return np.nan

    @staticmethod
    def get_date(row):
        return row['published_at'][:7]

    @staticmethod
    def get_year(row):
        return row['published_at'][:4]


if __name__ == '__main__':
    # resp = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?date_req=01/03/2003')
    # resp_xml_content = resp.content
    # tree = etree.XML(resp_xml_content)
    # res = int(tree.xpath('/ValCurs/Valute/CharCode[text() = "USD"]/parent::*/Value/text()')[0])
    # print(resp.content)
    # print(res)
    demand = Demand()
