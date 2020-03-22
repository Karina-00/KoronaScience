from typing import List
import pandas as pd
import datetime
import os

# confirmed cases
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a9f182afe873ce7e65d2307fcf91013c23a4556c" \
      f"/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
dfC = pd.read_csv(url, error_bad_lines=False)

# deaths
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a9f182afe873ce7e65d2307fcf91013c23a4556c" \
      f"/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
dfD = pd.read_csv(url, error_bad_lines=False)

# recovered cases
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/a9f182afe873ce7e65d2307fcf91013c23a4556c" \
      f"/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
dfR = pd.read_csv(url, error_bad_lines=False)


# Helper function (strftime not cross platform) ???
def format_date(date: datetime.date):
    if os.name == "nt":
        return date.strftime('%#m/%#d/%y')
    else:
        return date.strftime('%-m/%-d/%y')


def countries_with_no_deaths_count(date: datetime.date) -> int:
    date = format_date(date)
    razem = pd.merge(dfC, dfD, how="inner", on=["Country/Region", "Province/State"])

    result = razem.loc[razem[f"{date}_x"] > 0][razem[f"{date}_y"] == 0]
    nr = result[f"{date}_x"].count()
    return nr


def more_cured_than_deaths_indices(date: datetime.date) -> List[int]:
    date = format_date(date)
    razem = pd.merge(dfR, dfD, how="inner", on=["Province/State", "Country/Region"])
    result = razem[razem[f"{date}_x"] > razem[f"{date}_y"]]
    return list(result[["Country/Region", f"{date}_x", f"{date}_y"]].index)
