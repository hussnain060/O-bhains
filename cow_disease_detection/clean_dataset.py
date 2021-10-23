import pandas as pd
import gspread # pip install gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe


gc = gspread.service_account(filename='cow_disease_detection\credentials.json')
sh = gc.open_by_key("19u6J8J7G3DsvS3aPGJaa9NFNY_P3rfpIIh7X9i3wRfw")
worksheet = sh.sheet1

sheet1_df = get_as_dataframe(worksheet)
sheet1_df = sheet1_df.iloc[:, :6]
sheet1_df = sheet1_df.dropna()


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
print(df)
df.to_csv('file2.csv', index=False)