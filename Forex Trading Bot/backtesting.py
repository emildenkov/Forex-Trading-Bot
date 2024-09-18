import time
import datetime as dt

import yfinance as yf


short_window = 20
long_window = 50

initial_balance = 10000
balance = initial_balance
position = 0

forex_pair = 'EURUSD=X'


data = yf.download(forex_pair, period='5d', interval='1m', progress=False)

data['SMA_Short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['SMA_Long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

for index, row in data.iterrows():

    if row['SMA_Short'] > row['SMA_Long'] and position == 0:
        units_to_buy = balance // row['Close']
        balance -= units_to_buy * row['Close']
        position += units_to_buy

        print(f'{dt.datetime.now()}: Bought {units_to_buy} EUR for {row["Close"]:.2f} USD per unit')

    elif row['SMA_Short'] < row['SMA_Long'] and position > 1:
        balance += position * row['Close']

        print(f'{dt.datetime.now()}: Sold {position} EUR for {row["Close"]:.2f} USD per unit')

        position = 0

    else:
        print(f'{dt.datetime.now()}: Holding {position} EUR at {row["Close"]:.2f} USD per unit')

final_balance = balance + position * row['Close']
print(f'Final Balance: ${final_balance:.2f}')

if final_balance > initial_balance:
    print(f'Final balance increased by {(final_balance / initial_balance - 1) * 100:.2f}%')

elif final_balance < initial_balance:
    print(f'Final balance decreased by {(1 - final_balance / initial_balance) * 100:.2f}%')

else:
    print('Balance did not change!')