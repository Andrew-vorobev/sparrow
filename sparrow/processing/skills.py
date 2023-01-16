import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

VACANCIES_FILE = './data/vacancies_with_skills.csv'


class Demand:
    def __init__(self):
        self.df = pd.read_csv(VACANCIES_FILE, usecols=['name', 'key_skills', 'published_at'])
        self.df = self.df[self.df['name'].str.contains('|'.join(['ERP-специалист', 'erp', 'enterprise resource planning', 'abap', 'crm', 'help desk', 'helpdesk','service desk', 'servicedesk', 'bi', 'sap']), case=False)]
        self.df['key_skills'].replace('', np.nan, inplace=True)
        self.df.dropna(subset=['key_skills'], inplace=True)
        self.df['year'] = self.df['published_at'].apply(lambda p: p[:4])

        res = {}
        for year, group in self.df.groupby(['year']):
            res[year] = {}
            for _, row in group.iterrows():
                for skill in row['key_skills'].split('\n'):
                    if skill in res[year]:
                        res[year][skill] += 1
                    else:
                        res[year][skill] = 1
        dff = pd.DataFrame(res)

        i = 7
        for year in ('2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'):
            dfy = dff.sort_values(by=[year], ascending=False).head(10)
            res = dfy[year].to_dict()
            print(list(res.keys()))
            print(list(res.values()))

            fig, ax = plt.subplots(nrows=1, ncols=1)
            ax.bar(list(res.keys()), list(res.values()))
            ax.set_title(f'Топ 10 навыков для указанной профессии в {year} году:')
            ax.set_ylabel('Количество упоминаний')
            ax.set_xlabel('Навык')
            plt.xticks(rotation=90)
            plt.tight_layout()
            fig.savefig(f'image_{i}.png')

            i += 1


if __name__ == '__main__':
    demand = Demand()
