import csv
import typing
import unidecode

from dataclasses import dataclass


@dataclass
class Income:
    value: float
    country: str


@dataclass
class Cost:
    value: float
    country: str


@dataclass
class Performance:
    value: float
    country: str
    cost: Cost
    income: Income

    def as_dict(self) -> typing.Dict:
        return {
            "Performance %": self.value,
            "country": self.country,
            "cost": self.cost.value,
            "income": self.income.value,
        }


def process():
    incomes = get_incomes_from_admob()
    costs = get_costs_from_google_ads()
    countries = group_country_by_income_and_cost(incomes, costs)
    performances = sort_performances(compute_performance(countries))
    save_as_csv(performances)


def save_as_csv(performances: typing.List[Performance]):
    keys = performances[0].as_dict().keys()

    with open('csv/performances.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()

        performances_as_dict = []
        for performance in performances:
            performances_as_dict.append(performance.as_dict())
        dict_writer.writerows(performances_as_dict)


def sort_performances(performances: typing.List[Performance]) -> typing.List[Performance]:
    performances.sort(key=lambda performance: performance.value, reverse=True)
    return performances


def compute_performance(countries: typing.Dict[str, typing.Tuple[Income, Cost]]) -> typing.List[Performance]:
    performances = []
    for country, income_and_cost in countries.items():
        income, cost = income_and_cost
        value = (income.value * 100 / cost.value) - 100
        performance = Performance(value=value, country=country, income=income, cost=cost)
        performances.append(performance)

    return performances


def group_country_by_income_and_cost(incomes: typing.List[Income], costs: typing.List[Cost]) \
        -> typing.Dict[str, typing.Tuple[Income, Cost]]:
    countries = {}
    for income in incomes:
        for cost in costs:
            # ignore accents

            income_country = unidecode.unidecode(income.country.lower())
            cost_country = unidecode.unidecode(cost.country.lower())

            if income_country == cost_country:
                countries[cost.country] = (income, cost)

    return countries


def get_incomes_from_admob() -> typing.List[Income]:
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


def get_costs_from_google_ads() -> typing.List[Cost]:
    start_content_row_index = 3
    cost_column_index = 3
    country_column_index = 0

    costs = []
    with open('csv/google_ads.csv', 'r', encoding='utf-16') as csvfile:
        rows = csv.reader(csvfile, delimiter='	', quotechar='|')
        for index, row in enumerate(rows):
            if index >= start_content_row_index:
                value = float(row[cost_column_index].replace("\"", "").replace(",", "."))
                costs.append(Cost(value=value, country=row[country_column_index]))

    # remove last rows because
    costs.pop()
    costs.pop()
    return costs
