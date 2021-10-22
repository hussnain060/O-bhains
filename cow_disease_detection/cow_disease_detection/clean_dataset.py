import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gc = gspread.authorize(GoogleCredentials.get_application_default())

""" When below section run ... a url show click on url and login with your account it... copy sign in key and paste it into text box and press enter

"""

sheet_url = "https://docs.google.com/spreadsheets/d/1AJSGHiLQvwlPYY7RPyS7nlYwLmof70DC-NVHT-o7QtE/edit?usp=drivesdk"
sheet_id = gc.open_by_url(sheet_url)

ws = sheet_id.worksheet("Sheet1")

# Google sheet Data

sheet1_df = get_as_dataframe(ws)
sheet1_df = sheet1_df.iloc[:, :6]
sheet1_df = sheet1_df.dropna()
sheet1_df

# Download DataFrame as CSV file

sheet1_df.to_csv('file1.csv', index=False)

sheet1_df.info()

# Average Temperature and movement of cow per day

date_df = sheet1_df['date'].drop_duplicates()
days_temperature_avg = []
days_X_axis_avg = []
days_Y_axis_avg = []
days_Z_axis_avg = []
for x in date_df:
    days_data = sheet1_df.loc[sheet1_df['date'] == x]
    days_temperature_avg.append(days_data['temperature'].sum() / len(days_data['temperature']))
    days_X_axis_avg.append(days_data['x_axix'].sum() / len(days_data['x_axix']))
    days_Y_axis_avg.append(days_data['y_axix'].sum() / len(days_data['y_axix']))
    days_Z_axis_avg.append(days_data['z_axix'].sum() / len(days_data['z_axix']))

df = pd.DataFrame({
    'Date': date_df,
    'Temperature_avg': days_temperature_avg,
    'X_axis_avg': days_X_axis_avg,
    'Y_axis_avg': days_Y_axis_avg,
    'Z_axis_avg': days_Z_axis_avg
})
df = df.round(2)

# Final dataset

df.to_csv('file2.csv', index=False)