# Crypto convert
Simple script to calculate balance of total owned crypto currencies based on previous transactions. Makes use of the https://www.cryptocompare.com/ API to get current and historic prices/exchange rates.

## Usage
```
git clone https://github.com/mar-muel/crypto_convert.git && cd crypto_convert
pip install -r requirements.txt
cp transactions.csv.example transactions.csv
# Change transactions.csv file and fill in your own transactions
python balance.py
```
Example input (`transactions.csv`):

| Time  | Origin currency | Origin amount | Target currency |
| ------------- | ------------- | ------------- | ------------- |
| 22/12/16 00:41  | EUR | 1000 | BTC |
| 23/12/16 15:15  | EUR | 500 | ETH |
| 22/12/17 15:15  | BTC | 1 | EUR |

Make sure to use the same timestamp format and currency code abbreviations (according to https://www.cryptocompare.com/coins/).

Output:
```
---------------------------
Currency: BTC (5.90%)
Current amount:	 BTC    0.21100
Current value:	 EUR    2650.26
--------------------------
Currency: ETH (94.10%)
Current amount:	 ETH   67.90000
Current value:	 EUR   42248.06
--------------------------
Net balance of fiat:	EUR   10367.06
Net value of cryptos:	EUR   44898.32
Total win/loss:		EUR   55265.38
```

## Output to any fiat currency
```
python balance.py -f CAD
```
By default picks fiat currency from list of transactions if no output currency is set. Supported fiat currencies are: `["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "USD", "ZAR"]`

Enjoy :beers:!
