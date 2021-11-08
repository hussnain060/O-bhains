import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("file2.csv")
x = df['Date']
y = df['Temperature_avg']
plt.figure(figsize=(9, 5))
plt.plot(x, y)
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.title("Cow Temperature")
plt.grid(axis='y')

tt = df['Date']
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(tt, df.X_axis_avg, label='x-axis')
ax.plot(tt, df.Y_axis_avg, label='y-axis')
ax.plot(tt, df.Z_axis_avg, label='z-axis')
ax.set_xlabel("Date")
ax.set_ylabel("Axis")
ax.set_title("Cow movement along with Axis")
ax.grid(axis='y')
ax.legend()

date_per_day = list(df['Date'])
temperature = list(df['Temperature_avg'])

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(date_per_day, temperature, color='blue',
        width=0.4)

plt.xlabel("Date")
plt.ylabel("Temperature")
plt.title("Average Temperature of Cow")
plt.grid(axis='y')
plt.show()