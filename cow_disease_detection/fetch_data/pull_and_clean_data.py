import pandas as pd
import argparse
import gspread
from gspread_dataframe import get_as_dataframe

"""This module is use to access,preporcess & summarize data 
from google sheet. Three files (raw_data,clean_data & 
summarized_data) are saved to the following directory: 
./cow_disease_detection/data/ 


Example
-------
    $ python pull_and_clean_data.py --average_by day --from_date 2021-12-31

Functions
--------
1. argument_parser
2. get_data
3. data_preprocessing
4. summarize_data
"""


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
        default="hour",
        dest="average_by",
        help="Summarized the data by average",
        choices=["month", "week", "day", "hour", "minute"],
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


def get_data() -> pd.DataFrame:
    """This function pull data from google account
    Saves the data to:
    ./cow_disease_detection/data/ 
    as raw_data.csv
    TODO: use secrets in the future to hide credentials

    Parameters
    ----------
    NULL

    Returns
    -------
    pd.DataFrame
        This function return a pandas dataset.


    """

    file = "./cow_disease_detection/fetch_data/credentials.json"
    key = "1AJSGHiLQvwlPYY7RPyS7nlYwLmof70DC-NVHT-o7QtE"

    # pull data
    gc = gspread.service_account(filename=file)
    sh = gc.open_by_key(key)
    worksheet = sh.sheet1
    df = get_as_dataframe(worksheet)
    # save to disk
    df.to_csv("./cow_disease_detection/data/raw_data.csv", index=False)
    return df


# data preprocessing
def data_preprocessing(input_data: pd.DataFrame) -> pd.DataFrame:
    """This function does the following processing on the fetch data:
    1. Remove unnecessary columns. 
    2. Drop records where any feature is blank.
    3. Create a date_time column.
    4. Generate more time features such as year,month,week,day,hour,minute.
    
    Output is saved to:
    ./cow_disease_detection/data/ 
    as clean_data.csv


    Parameters
    ----------
    input_data : pd.DataFrame
        Raw data produced by the get_data() function.

    Returns
    -------
    DataFrame
        Returns a cleaned and preprocessed dataset.

    """
    df = get_data()  # input data.copy()
    # remove 'unnamed' columns
    df = df.loc[:, ~df.columns.str.contains("Unnamed:")]
    # drop null records
    df = df.dropna()

    # concatenate date and time column
    date_time = pd.to_datetime(df["date"] + " " + df["time"])
    # insert date_time column at the beginning
    df.insert(loc=0, column="date_time", value=date_time)
    # drop date and time columns
    df = df.drop(["date", "time"], axis=1)

    # generate time dimensions
    df["year"] = df["date_time"].dt.year
    df["month"] = df["date_time"].dt.month
    df["week"] = df["date_time"].dt.isocalendar().week
    df["day"] = df["date_time"].dt.day
    df["hour"] = df["date_time"].dt.hour
    df["minute"] = df["date_time"].dt.minute

    # save
    df.to_csv("./cow_disease_detection/data/clean_data.csv", index=False)

    return df


def summarize_data(average_by: str, input_data: pd.DataFrame) -> pd.DataFrame:
    """This function summarizes temperature and movements of a 
    cow by taking the average (median) measurements.

    Output is saved to:
    ./cow_disease_detection/data/ 
    as summarized_data.csv

    Parameters
    ----------
    average_by : str
        average movements and temperature. By default "hour"
        Possible options are
        "month", "week", "day", "hour", "minute"
    
    input_data: pd.DataFrame
        processed data frame from the data_preprocessing ()

    Returns
    -------
    DataFrame
        This function returns summarized data

    """

    # remove data_time column, for summary we do not need it
    input_data.drop(columns=["date_time"], inplace=True)

    # list of availabe options for summary
    options = ["month", "week", "day", "hour", "minute"]
    # determine what are the levels required for grouping
    _index = options.index(average_by)
    group_by = options[: _index + 1]

    # get average
    t1 = ("temperature", "median")
    t2 = ("x_axix", "median")
    t3 = ("y_axix", "median")
    t4 = ("z_axix", "median")
    # groupby
    df_gb = input_data.groupby(group_by)
    # apply average function
    df_gb = df_gb.agg(avg_temp=t1, avg_x=t2, avg_y=t3, avg_z=t4)
    # reset index
    df_gb.reset_index(inplace=True)
    # save to disk
    df_gb.to_csv("./cow_disease_detection/data/summarized_data.csv", index=False)

    return None  # update_df


if __name__ == "__main__":
    arguments = argument_parser()
    data = get_data()
    data = data_preprocessing(data,)
    data = summarize_data(arguments.average_by, data)
    del data

