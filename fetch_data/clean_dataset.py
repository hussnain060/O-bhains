import pandas as pd

# pip install gspread if required
import gspread

# pip install gspread_dataframe if required
from gspread_dataframe import get_as_dataframe, set_with_dataframe


gc = gspread.service_account(filename="./fetch_data/credentials.json")
sh = gc.open_by_key("1AJSGHiLQvwlPYY7RPyS7nlYwLmof70DC-NVHT-o7QtE")
worksheet = sh.sheet1

sheet1_df = get_as_dataframe(worksheet)
sheet1_df = sheet1_df.iloc[:, :6]
sheet1_df = sheet1_df.dropna()


# Dataset
print(sheet1_df)
sheet1_df.to_csv("./data/from_fetch_data.csv", index=False)
