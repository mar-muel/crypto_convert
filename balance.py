import pandas as pd
import requests


def main():
    # Read data
    df = pd.read_csv('transactions.csv')
    df.dropna(axis=0, how='all', inplace=True)
    df['Time'] = pd.to_datetime(df['Time'], format="%d/%m/%y %H:%M")
    df = df.sort_values(by='Time')

    # params
    fiat_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "USD", "ZAR"]
    fiat = 'EUR'
    base_uri = 'https://www.cryptocompare.com/api/data/'
    base_uri_min = 'https://min-api.cryptocompare.com/data/'

    # validate input
    url_coinlist = base_uri + 'coinlist/'
    resp = requests.get(url_coinlist)
    if resp.status_code != 200:
        raise Exception("Could not make API call to {}".format(base_uri))
    available_currencies = resp.json()['Data'].keys()
    currencies = set(df['Origin currency']).union(df['Target currency'])
    for c in currencies:
        if c not in available_currencies and c not in fiat_currencies:
            raise Exception("Currency {} is not available or not valid fiat currency. Check {} for available currencies.".format(c, url_coinlist))

    # compute balance
    balance = {k:{'amount':0.0} for k in currencies}
    for i, row in df.iterrows():
        url = base_uri_min + "pricehistorical?fsym={}&tsyms={}&ts={}".format(row['Origin currency'], row['Target currency'], int(row['Time'].timestamp()))
        res = requests.get(url)
        exchange_rate = float(res.json()[row['Origin currency']][row['Target currency']])
        balance[row['Origin currency']]['amount'] -= row['Origin amount']
        balance[row['Target currency']]['amount'] += row['Origin amount'] * exchange_rate

    # convert to fiat
    for currency in balance.keys():
        url = base_uri_min + 'price?fsym={}&tsyms={}'.format(currency, fiat)
        response = requests.get(url).json()
        price_per_fiat = response[fiat]
        balance[currency]['value_fiat'] = balance[currency]['amount'] * price_per_fiat

    balance = pd.DataFrame(balance)

    # write output
    total_val_crypto_in_fiat = balance.loc[:, balance.columns != fiat].loc['value_fiat'].sum()
    net_balance = total_val_crypto_in_fiat + balance[fiat]['amount']
    print('---------------------------')
    for currency in balance:
        if not currency == fiat:
            fractional_value = balance[currency]['value_fiat'] / total_val_crypto_in_fiat
            print('Currency: {} ({:2.2%})'.format(currency, fractional_value))
            print('Current amount:\t {} {:10.5f}'.format(currency, balance[currency]['amount']))
            print('Current value:\t {} {:10.2f}'.format(fiat, balance[currency]['value_fiat']))
            print('--------------------------')

    print('Net balance of fiat:\t{} {:10.2f}'.format(fiat, balance[fiat]['amount']))
    print('Net value of cryptos:\t{} {:10.2f}'.format(fiat, total_val_crypto_in_fiat))
    print('Total win/loss:\t\t{} {:10.2f}'.format(fiat, net_balance))



if __name__ == "__main__":
    main()
