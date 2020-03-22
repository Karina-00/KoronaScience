from typing import List

import pandas as pd

CONFIRMED_CASES_URL = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                      f"/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv "


confirmed_cases = pd.read_csv(CONFIRMED_CASES_URL, error_bad_lines=False)


def poland_cases_by_date(day: int, month: int, year: int = 2020) -> int:
    year = str(year)[2:]
    return confirmed_cases.loc[confirmed_cases["Country/Region"] == "Poland"][f"{month}/{day}/{year}"].values[0]


def top5_countries_by_date(day: int, month: int, year: int = 2020) -> List[str]:
    year = str(year)[2:]
    date = f'{month}/{day}/{year}'

    x = confirmed_cases[["Country/Region", date]].sort_values(by=date)
    new_df = x.groupby("Country/Region").sum().sort_values(by=date).tail(5).sort_values(by=date, ascending=False)

    result = list(new_df.T)
    return result


def no_new_cases_count(day: int, month: int, year: int = 2020) -> int:
    year = str(year)[2:]
    date = f'{month}/{day}/{year}'

    columns = list(confirmed_cases)
    idx = columns.index(date)
    day_before = columns[idx-1]

    data_set = confirmed_cases[["Country/Region", day_before, date]]
    confirmed_cases['new_today'] = confirmed_cases[date] - confirmed_cases[day_before]
    new_cases = confirmed_cases.loc[confirmed_cases['new_today'] != 0].count()[-1]
    return new_cases
