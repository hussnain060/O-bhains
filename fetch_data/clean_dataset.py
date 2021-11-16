import pandas as pd
import argparse

# pip install gspread if required
import gspread

# pip install gspread_dataframe if required
from gspread_dataframe import get_as_dataframe, set_with_dataframe

# getting data form google sheet
gc = gspread.service_account(filename="./fetch_data/credentials.json")
sh = gc.open_by_key("1AJSGHiLQvwlPYY7RPyS7nlYwLmof70DC-NVHT-o7QtE")
worksheet = sh.sheet1
df = get_as_dataframe(worksheet)

# data preprocessing
df = df.iloc[:, :6]
df = df.dropna()

df["date"] = pd.to_datetime(
    df["date"] + " " + df["time"]
)  # concatenate date and time column
df = df.drop("time", axis=1)
df = df.rename(columns={"date": "datetime"})

# passing arguments to average dataset
parse = argparse.ArgumentParser(description="modify dataset")
parse.add_argument(
    "--average_by",
    type=str,
    help="Average dataset by days/hours/no average",
    choices=["days", "hours", "no avg"],
)


def avg(average, dataset):
    """This function is used for Average Temperature and movement of cow per days/per hours
    You just pass one argument:
    1. Average by hours/days
    """
    update_df = dataset
    times = pd.DatetimeIndex(dataset.datetime)
    if average == "days":  # Average Temperature and movement of cow per days
        update_df = dataset.groupby([times.date])[
            ["temperature", "x_axix", "y_axix", "z_axix"]
        ].median()
    elif average == "hours":  # Average Temperature and movement of cow per hours
        update_df = dataset.groupby([times.date, times.hour])[
            ["temperature", "x_axix", "y_axix", "z_axix"]
        ].median()

    return update_df


if __name__ == "__main__":
    arg = parse.parse_args()
    df = avg(arg.average_by, df)

    # Dataset
    print(df.head(10))
    print(avg.__doc__)
    df.to_csv("./data/from_fetch_data.csv", index=False)
