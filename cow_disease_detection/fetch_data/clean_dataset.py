import pandas as pd
import argparse
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

"""This module is use to access data from google sheet,
preprocess data, average data by days/hours (if you need),
make csv formate file and stored in data folder.

Example
-------
    $ python clean_dataset.py --days/hours (optional arguments)

Attributes
----------
NULL

Function
--------
1. get_data()
2. data_preprocessing()
3. calculate_average()
"""


def get_data() -> "DataFrame":
    """This function Getting data form google sheet.

    Parameters
    ----------
    NULL

    Returns
    -------
    DataFrame
        This function return a dataset.

    Example
    --------
    >>> get_data()
    'Dataframe'
    """
    gc = gspread.service_account(
        filename="./cow_disease_detection/fetch_data/credentials.json"
    )
    sh = gc.open_by_key("1AJSGHiLQvwlPYY7RPyS7nlYwLmof70DC-NVHT-o7QtE")
    worksheet = sh.sheet1
    df = get_as_dataframe(worksheet)
    return df


# data preprocessing
def data_preprocessing() -> "DataFrame":
    """this function preprocess data that get from google sheet.

    Parameters
    ----------
    NULL

    Returns
    -------
    DataFrame
        This function return a dataset.

    Example
    --------
    >>> data_preprocessing()
    'Dataframe'
    """
    df = get_data()
    df = df.iloc[:, :6]
    df = df.dropna()
    df["date"] = pd.to_datetime(
        df["date"] + " " + df["time"]
    )  # concatenate date and time column
    df = df.drop("time", axis=1)
    df = df.rename(columns={"date": "datetime"})
    return df


def argument_parser():
    """This function captures the comandline arguments for clean_dataset module"""
    # passing arguments to average dataset
    parse = argparse.ArgumentParser(description="summarize the dataset by average")

    # summary option
    parse.add_argument(
        "-a",
        "--average_by",
        type=str,
        required=False,
        default="day",
        dest="average_by",
        help="Summarized the data by average",
        choices=["month", "week", "day", "hour", "minute", "none"],
    )

    #
    parse.add_argument(
        "-f",
        "--from_date",
        type=str,
        required=False,
        default="2021-01-01",
        dest="pull_data_from_date",
        help="To pull historical data from a specific date  e.g 2021-12-31",
    )

    return parse.parse_args()


def calculate_average(average_by: str) -> pd.DataFrame:
    """This function is used for Average Temperature and movement of cow per days/per hours.
    This function run at the start of the program and we give one argument so that function
    run properly.

    Parameters
    ----------
    average_by : str
        input data average by (days/hours/no avg)

    Returns
    -------
    DataFrame
        This function return dataset of days average, hours average, or no average.

    Example
    --------
    >>> calculate_average(days/hours/no avg)
    'Dataframe'
    """
    update_df = data_preprocessing()
    times = pd.DatetimeIndex(update_df.datetime)
    if average_by == "days":  # Average Temperature and movement of cow per days
        update_df = update_df.groupby([times.date])[
            ["temperature", "x_axix", "y_axix", "z_axix"]
        ].median()
        update_df.index.name = "days"
    elif average_by == "hours":  # Average Temperature and movement of cow per hours
        update_df = update_df.groupby([times.date, times.hour])[
            ["temperature", "x_axix", "y_axix", "z_axix"]
        ].median()
        update_df.to_csv("./cow_disease_detection/data/from_fetch_data.csv", index=True)
        update_df = pd.read_csv(
            "./cow_disease_detection/data/from_fetch_data.csv",
            sep=",",
            names=["days", "hours", "temperature", "x_axix", "y_axix", "z_axix"],
        )
        update_df.drop(update_df.head(1).index, inplace=True)

    return update_df


if __name__ == "__main__":
    arguments = argument_parser()
    df = calculate_average(average_by=arguments.average_by)

    # Dataset
    print(df.head(10))
    df.to_csv("./cow_disease_detection/data/from_fetch_data.csv", index=True)
