from pandas_datareader import data
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

_long =  data.DataReader("ITUB4.SA", "yahoo", datetime(2016,6,17), datetime.today())
_short = data.DataReader("ITSA4.SA", "yahoo", datetime(2016,6,17), datetime.today())

c_long = _long["Close"]
c_short = _short["Close"]

ls = pd.concat([c_long,c_short], axis=1)

print(ls)

print('Valor operacao SHORT: ' + str(7.3*600+7.21*560))
print('Valor operacao LONG: ' + str(29.12*300))

last_long_value = _long["Close"][len(_long)-1]
last_short_value = _short["Close"][len(_short)-1]

print('Valor atual SHORT: '+ str(last_short_value*1160))
print('Valor atual LONG: '+ str(last_long_value*300))

print('Ratio: '+ str(last_long_value/last_short_value))

spread = last_long_value*300 - last_short_value*1160 

print('Spread: '+str(spread))

btcValue = 366.57

print('Lucro liquido: ' + str(spread-btcValue))


#ls.plot()
#plt.show()
