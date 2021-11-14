import pandas as pd

# pip install gspread if required
import gspread

# pip install gspread_dataframe if required
from gspread_dataframe import get_as_dataframe, set_with_dataframe

gc = gspread.service_account(filename="./fetch_data/credentials.json")
sh = gc.open_by_key("1AJSGHiLQvwlPYY7RPyS7nlYwLmof70DC-NVHT-o7QtE")
worksheet = sh.sheet1
#
df = get_as_dataframe(worksheet)
df = df.iloc[:, :6]
df = df.dropna()
df['date'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df = df.drop('time', axis=1)
df = df.rename(columns={'date':'datetime'})
print(df)

df = pd.read_csv(".\\data\\from_fetch_data.csv")

i = input("Do you want to average data (y/n): ")
if i.lower()=='y':
    print("Average by days (Press 1)")
    print("Average by hours (Press 2)")
    print("For No Average (Press 3)")
    j = int(input("Enter number: "))
    times = pd.DatetimeIndex(df.datetime)
    if j==1:
        # Average Temperature and movement of cow per days
        df = df.groupby([times.date])[['temperature','x_axix','y_axix','z_axix']].median()
    elif j==2:
        # Average Temperature and movement of cow per hours
        df = df.groupby([times.date, times.hour])[['temperature','x_axix','y_axix','z_axix']].median()
    else:
        pass
else:
    pass

Dataset
print(df.head())
df.to_csv(".\\data\\from_fetch_data.csv", index=False)
