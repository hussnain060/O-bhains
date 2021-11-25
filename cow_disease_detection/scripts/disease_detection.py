import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("./cow_disease_detection/data/from_fetch_data.csv")
x = df['days']
y = df['temperature']
plt.figure(figsize=(9, 5))
plt.plot(x, y)
plt.xlabel('Days')
plt.ylabel('Temperature')
plt.title("Cow Temperature")
plt.grid(axis='y')

tt = df['days']
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(tt, df.x_axix, label='x-axis')
ax.plot(tt, df.y_axix, label='y-axis')
ax.plot(tt, df.z_axix, label='z-axis')
ax.set_xlabel("Date")
ax.set_ylabel("Axis")
ax.set_title("Cow movement along with Axis")
ax.grid(axis='y')
ax.legend()

date_per_day = list(df['days'])
temperature = list(df['temperature'])

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(date_per_day, temperature, color='blue',
        width=0.4)

plt.xlabel("Date")
plt.ylabel("Temperature")
plt.title("Average Temperature of Cow")
plt.grid(axis='y')
plt.show()
