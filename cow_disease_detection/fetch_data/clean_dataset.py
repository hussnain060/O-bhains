import pandas as pd
import argparse
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

"""This module is use to access data from google sheet,
preprocess data, average data by days/hours (if you need),
make csv formate file and stored in data folder.

Example
-------
    $ python clean_dataset.py

Attributes
----------
NULL

"""

def get_data():
    """Getting data form google sheet.

    Extended description of function.

    Parameters
    ----------
    NULL

    Returns
    -------
    dataframe
        return dataset that get from googlesheet.

    Example
    --------
    >>> get_data()
    'Dataframe'
    """
    gc = gspread.service_account(filename="./fetch_data/credentials.json")
    sh = gc.open_by_key("1AJSGHiLQvwlPYY7RPyS7nlYwLmof70DC-NVHT-o7QtE")
    worksheet = sh.sheet1
    df = get_as_dataframe(worksheet)
    return df


# data preprocessing
def data_preprocessing():
    """Data preprocessing.

    Extended description of function.

    Parameters
    ----------
    NULL

    Returns
    -------
    dataframe
        return dataset that get from get_data function.

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

# passing arguments to average dataset
parse = argparse.ArgumentParser(description="modify dataset")
parse.add_argument(
    "--average_by",
    type=str,
    help="Average dataset by days/hours/no average",
    choices=["days", "hours", "no avg"],
)

def avg(average):
    """This function is used for Average Temperature and movement of cow per days/per hours.
    This function run at the start of the program and we give one argument so that function
    run properly.

    Extended description of function.

    Parameters
    ----------
    arg1 : str
        input data average by (days/hours/no avg)

    Returns
    -------
    dataframe
        return dataset with days average, hours average, or no average.

    Example
    --------
    >>> avg(days/hours/no avg)
    'Dataframe'
    """
    update_df = data_preprocessing()
    # times = pd.DatetimeIndex(update_df.datetime)
    if average == "days":  # Average Temperature and movement of cow per days
        update_df = update_df.groupby(["date"])[
            ["temperature", "x_axix", "y_axix", "z_axix"]
        ].median()
    elif average == "hours":  # Average Temperature and movement of cow per hours
        update_df = update_df.groupby([times.date, times.hour])[
            ["temperature", "x_axix", "y_axix", "z_axix"]
        ].median()
        pass

    # return update_df

if __name__ == "__main__":
    arg = parse.parse_args()
    df = avg('days')

    # Dataset
    print(df.head(10))
    # print(avg.__doc__)
    df.to_csv("./data/from_fetch_data.csv", index=False)
