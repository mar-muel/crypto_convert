import pandas as pd
import requests
import argparse
import warnings


def main():
    # Read data
    df = pd.read_csv('transactions.csv')
    df.dropna(axis=0, how='all', inplace=True)
    df['Time'] = pd.to_datetime(df['Time'], format="%d/%m/%y %H:%M")
    df = df.sort_values(by='Time')

    # params
    fiat_currencies = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "USD", "ZAR"]
    base_uri = 'https://www.cryptocompare.com/api/data/'
    base_uri_min = 'https://min-api.cryptocompare.com/data/'
    
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fiat", type=str, choices=fiat_currencies, default='', help="Convert output into your favourite fiat currency. If not given, will pick your fiat from your transactions.")
    args = parser.parse_args()
    fiat = args.fiat

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
        if fiat == '' and c in fiat_currencies:
            fiat = c
    if fiat == '':
        warnings.warn("No fiat currency detected in transactions, fall back to USD.", RuntimeWarning)
        fiat = 'USD' 
        
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
        balance[currency]['price'] = price_per_fiat

    balance = pd.DataFrame(balance)

    # write output
    total_val_crypto_in_fiat = balance.loc[:, [b for b in balance.columns if b not in fiat_currencies]].loc['value_fiat'].sum()
    total_val_fiat = balance.loc[:, [b for b in balance.columns if b in fiat_currencies]].loc['value_fiat'].sum()
    net_balance = total_val_crypto_in_fiat + total_val_fiat
    print('---------------------------')
    for currency in balance:
        if currency not in fiat_currencies:
            fractional_value = balance[currency]['value_fiat'] / total_val_crypto_in_fiat
            print('Currency: {} ({:2.2%})'.format(currency, fractional_value))
            print('Current amount:\t\t {} {:10.5f}'.format(currency, balance[currency]['amount']))
            print('Current value:\t\t {} {:10.2f}'.format(fiat, balance[currency]['value_fiat']))
            print('Current price per 1 {}: {} {:10.2f}'.format(currency ,fiat, balance[currency]['price']))
            print('--------------------------')

    print('Net balance of fiat:\t{} {:10.2f}'.format(fiat, total_val_fiat))
    print('Net value of cryptos:\t{} {:10.2f}'.format(fiat, total_val_crypto_in_fiat))
    print('Total win/loss:\t\t{} {:10.2f}'.format(fiat, net_balance))



if __name__ == "__main__":
    main()
