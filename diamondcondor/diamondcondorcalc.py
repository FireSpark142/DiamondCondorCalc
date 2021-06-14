# -*- coding: utf-8 -*-

def main():
    import datetime
    f1 = datetime.date.today()
    while f1.weekday() != 4:
          f1 += datetime.timedelta(1)

    f2 = datetime.date.today()
    while f2.weekday() != 4:
          f2 += datetime.timedelta(1)

    import requests


    ticker = input("Enter desired stock ticker: ")

    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
        params={'symbol': ticker, 'expiration': f1, 'greeks': 'true'},
        headers={'Authorization': 'Bearer <token>', 'Accept': 'application/json'}
    )
    f1json_response = response.json()

    import requests


    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
        params={'symbol': ticker, 'expiration': f2, 'greeks': 'true'},
        headers={'Authorization': 'Bearer <token>', 'Accept': 'application/json'}
    )
    f2json_response = response.json()

    import pandas as pd

    f1df = pd.DataFrame(f1json_response['options']['option'])
    f1dfg = pd.DataFrame.from_records(f1df['greeks'])
    f1dfc = pd.concat([f1df,f1dfg],axis=1)

    import pandas as pd

    f2df = pd.DataFrame(f2json_response['options']['option'])
    f2dfg = pd.DataFrame.from_records(f2df['greeks'])
    f2dfc = pd.concat([f2df,f2dfg],axis=1)

    import requests

    response = requests.get('https://api.tradier.com/v1/markets/quotes',
        params={'symbols': ticker, 'greeks': 'false'},
        headers={'Authorization': 'Bearer <token>', 'Accept': 'application/json'}
    )
    json_response = response.json()
    import pandas as pd

    df = pd.DataFrame(json_response['quotes']['quote'],index=[0])

    last = df['last']

    for i in last:
      lsv = i

    def cover_call_strike_price():

      for i,v in zip(f1dfc['strike'],f1dfc['option_type']):
          if i > lsv and v == 'call':
            x = i
            return i

    def cash_covered_put_price(input):
      for i,v in zip(f1dfc['strike'],f1dfc['option_type']):
          if i > input and v == 'put':
            x = i
            return i

    def optimal_long_put():
      x = f2dfc[(f2dfc == 'put').any(axis=1)]

      df = pd.DataFrame()

      y = x['strike'].diff()
      z = x['ask'].diff()

      q=pd.concat([x['ask'],x['strike'], y, z], axis=1, keys=["ask", "strike","strikediff","askdiff"])

      q['diff'] = (q.askdiff - q.strikediff)

      q = q.astype(float)

      cinco = float(cash_covered_put_price(cover_call_strike_price()))

      quad = q[(q['strike'] > cinco)]

      tres = quad[(quad['diff'] < 0)]

      duo = tres.groupby("diff").max()

      return duo.iloc[0]

    t = cover_call_strike_price()
    u = cash_covered_put_price(cover_call_strike_price())
    v = optimal_long_put()['strike']

    print(f'Covered Call Strike for {ticker}: {t}, Cash Covered Put Strike for {ticker}: {u}, Optimal Long Put Strike for {ticker}: {v}')