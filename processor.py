import csv
from dataclasses import dataclass


@dataclass
class Income:
    value: float
    country: str


@dataclass
class Cost:
    value: float
    country: str


def process():
    incomes = get_incomes_from_admob()
    costs = get_costs_from_google_ads()
    print(costs)


def get_incomes_from_admob():
    start_content_row_index = 1
    income_column_index = 9
    country_column_index = 0

    incomes = []
    with open('csv/admob.csv', 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter='	', quotechar='|')
        for index, row in enumerate(rows):
            if index >= start_content_row_index:
                value = float(row[income_column_index].replace("\"", "").replace(",", "."))
                incomes.append(Income(value=value, country=row[country_column_index]))
    return incomes


def get_costs_from_google_ads():
    start_content_row_index = 3
    cost_column_index = 3
    country_column_index = 0

    costs = []
    with open('csv/google_ads.csv', 'r', encoding='utf-16') as csvfile:
        rows = csv.reader(csvfile, delimiter='	', quotechar='|')
        for index, row in enumerate(rows):
            if index >= start_content_row_index:
                value = float(row[cost_column_index].replace("\"", "").replace(",", "."))
                costs.append(Income(value=value, country=row[country_column_index]))

    # remove last rows because
    costs.pop()
    costs.pop()
    return costs
