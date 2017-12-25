# Crypto convert
Simple script to calculate balance of total owned crypto currencies based on previous transactions. Makes use of the https://www.cryptocompare.com/ API to get current and historic prices/exchange rates.

# Usage
```
git clone https://github.com/mar-muel/crypto_convert.git
pip install -r requirements.txt
# Change transactions.csv file for your own currencies
python balance.py
```

Output:
```
---------------------------
Currency: BTC
Current amount:	 BTC    0.21100
Current value:	 EUR    2487.73
--------------------------
Currency: ETH
Current amount:	 ETH   67.90000
Current value:	 EUR   41554.12
--------------------------
Net balance of fiat:	EUR   10367.06
Net value of cryptos:	EUR   44041.85
Total win/loss:		EUR   54408.91
```

Enjoy :beers:!
