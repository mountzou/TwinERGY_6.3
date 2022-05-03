import requests
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()

power_loss_coefficient = -0.29/100
nominal_power = 220
n_inverter = 0.9

response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=37.9792&longitude=23.7166&hourly=temperature_2m,direct_normal_irradiance,windspeed_10m&windspeed_unit=ms")

json_weather_Data = json.loads(response.text)

array_of_temperatures = json_weather_Data['hourly']['temperature_2m']

array_of_irradiance = json_weather_Data['hourly']['direct_normal_irradiance']

array_of_wind_speed = json_weather_Data['hourly']['windspeed_10m']

array_of_time = json_weather_Data['hourly']['time']

data = np.array([array_of_temperatures])

array = [array_of_temperatures, array_of_irradiance, array_of_wind_speed]

df = pd.DataFrame(zip(array_of_temperatures, array_of_irradiance, array_of_wind_speed), columns=['Ambient Temperature','Direct Irradiance','Windspeed'], index=array_of_time)

df['Tpv'] = df['Ambient Temperature'] + 0.32*df['Direct Irradiance']/(8.91 + 2.98*df['Windspeed'])

df['Pdc'] = 0.001*df['Direct Irradiance']*nominal_power*(1 + power_loss_coefficient * (df['Tpv']-25))

df['Pac'] = df['Pdc']*n_inverter

df['Date'] = df.index

df['Date'] = df['Date'].astype('datetime64[ns]')

df.set_index('Date', inplace = True)

df_daily = df[['Pac']].resample('1D').sum()

print(df_daily)