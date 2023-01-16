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
        self.df = pd.read_csv(VACANCIES_FILE, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name'])
        self.df['average'] = self.df[['salary_from', 'salary_to']].mean(axis=1)
        self.df['salary'] = self.df.apply(self.get_salary, axis=1)
        self.df.dropna(subset=['salary'], inplace=True)

        # df2 = self.df[self.df['name'].str.contains('|'.join(['ERP-специалист', 'erp', 'enterprise resource planning', 'abap', 'crm', 'help desk', 'helpdesk', 'service desk', 'servicedesk', 'bi', 'sap']), case=False)]

        new_df = pd.DataFrame({'salary': self.df.groupby(['area_name'])['salary'].mean()}).reset_index()
        # new_df['salary'] =
        new_df = new_df.sort_values(by=['salary'], ascending=False)[1:21]
        # new_df = new_df.head(10)

        # new_df2 = pd.DataFrame()
        # new_df2['count'] = self.df.groupby(['area_name']).size()
        new_df2 = pd.DataFrame({'count': self.df.groupby(['area_name']).size()}).reset_index()
        new_df2 = new_df2.sort_values(by=['count'], ascending=False).head(20)
        count = self.df.shape[0]
        new_df2['part'] = new_df2['count'].apply(lambda c: round(c / count, 4))
        # new_df2 = new_df2.head(20)


        # new_df['s_salary'] = df2.groupby(['year'])['salary'].mean()
        # new_df['s_count'] = df2.groupby(['year']).size()
        print(new_df)
        print(new_df2)
        # print(new_df['area_name'].to_list())
        # print(new_df.to_dict())

        # stats = new_df.to_dict()

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.bar(new_df['area_name'].to_list(), new_df['salary'].to_list())
        ax.set_title('Уровень зарплат по городам (в порядке убывания)')
        ax.set_ylabel('Зарплата, руб.')
        ax.set_xlabel('Город')
        plt.xticks(rotation=90)
        plt.tight_layout()
        # fig.autofmt_xdate()
        fig.savefig('image_5.png')

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.bar(new_df2['area_name'].to_list(), new_df2['part'].to_list())
        ax.set_title('Доля вакансий по городам (в порядке убывания)')
        ax.set_ylabel('Доля вакансий')
        ax.set_xlabel('Город')
        plt.xticks(rotation=90)
        plt.tight_layout()
        # fig.autofmt_xdate()
        fig.savefig('image_6.png')

    @staticmethod
    def get_salary(row):
        try:
            return row['average'] * currency_to_rub[row['salary_currency']]
        except:
            return np.nan


if __name__ == '__main__':
    demand = Demand()
