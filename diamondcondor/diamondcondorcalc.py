def hello_world(request):
    request_json = request.get_json()
    if request.args and 'ticker' in request.args:
        return main(request.args.get('ticker'))
    else:
        return 'Error - Please add ?ticker={insert ticker name here} to the end of the url'



def main(input):
    import datetime

    f1 = datetime.date.today()
    while f1.weekday() != 4:
        f1 += datetime.timedelta(1)

    f2 = datetime.date.today()
    while f2.weekday() != 4:
        f2 += datetime.timedelta(1)

    import requests

    ticker = input

    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
                            params={'symbol': ticker, 'expiration': f1, 'greeks': 'true'},
                            headers={'Authorization': 'Bearer <>', 'Accept': 'application/json'}
                            )
    f1json_response = response.json()

    import requests

    response = requests.get('https://api.tradier.com/v1/markets/options/chains',
                            params={'symbol': ticker, 'expiration': f2, 'greeks': 'true'},
                            headers={'Authorization': 'Bearer <>', 'Accept': 'application/json'}
                            )
    f2json_response = response.json()

    import pandas as pd

    f1df = pd.DataFrame(f1json_response['options']['option'])
    f1dfg = pd.DataFrame.from_records(f1df['greeks'])
    f1dfc = pd.concat([f1df, f1dfg], axis=1)

    f2df = pd.DataFrame(f2json_response['options']['option'])
    f2dfg = pd.DataFrame.from_records(f2df['greeks'])
    f2dfc = pd.concat([f2df, f2dfg], axis=1)

    import requests

    response = requests.get('https://api.tradier.com/v1/markets/quotes',
                            params={'symbols': ticker, 'greeks': 'false'},
                            headers={'Authorization': 'Bearer <>', 'Accept': 'application/json'}
                            )
    json_response = response.json()

    import pandas as pd

    df = pd.DataFrame(json_response['quotes']['quote'], index=[0])

    last = df['last']

    for i in last:
        lsv = i


    def cover_call_strike_price():
        for i, v, k in zip(f1dfc['strike'], f1dfc['option_type'], f1dfc['ask']):
            if i > lsv and v == 'call':
                x = [i, k]
                return x


    def cash_covered_put_price(input):
        for i, v, k in zip(f1dfc['strike'], f1dfc['option_type'], f1dfc['ask']):
            if i > input and v == 'put':
                z = [i, k]
                return z


    def optimal_long_put():
        x = f2dfc[(f2dfc == 'put').any(axis=1)]

        df = pd.DataFrame()

        y = x['strike'].diff()
        z = x['ask'].diff()

        q = pd.concat([x['ask'], x['strike'], y, z], axis=1, keys=["ask", "strike", "strikediff", "askdiff"])

        q['diff'] = (q.askdiff - q.strikediff)

        q = q.astype(float)

        cinco = float(cash_covered_put_price(cover_call_strike_price()[1])[1])

        quad = q[(q['strike'] > cinco)]

        tres = quad[(quad['diff'] < 0)]

        duo = tres.groupby("diff").max()

        return duo.iloc[0]


    t = cover_call_strike_price()
    u = cash_covered_put_price(cover_call_strike_price()[0])
    v = optimal_long_put()['strike']
    w = optimal_long_put()['ask']
    x = f' Covered Call Strike for {ticker}: {t[0]} || Cash Covered Put Strike for {ticker}: {u[0]} || Optimal Long Put Strike for {ticker}: {v} || Total cost of stock purchase = ${(lsv) * 200} USD || Total cost: ${((t[1] + u[1] + w) * 100) + ((lsv) * 200)} USD'
    return x
