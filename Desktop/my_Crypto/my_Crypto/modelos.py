import requests
from key import APIKEY

def valorCrypto(crypto):
    url = f'https://rest.coinapi.io/v1/exchangerate/{crypto}/EUR'
    headers = {'X-CoinAPI-Key' : APIKEY}
    response = requests.get(url, 
                            headers=headers)
    r = response.json()
    rate = r["rate"]
    return rate

def comprarCrypto(eur, 
                  crypto):
    rate = valorCrypto(crypto)
    total = eur / rate
    return total

def tradeoCrypto(q, 
                 crypto,
                 crypto2):
    q = float(q)
    url = f'https://rest.coinapi.io/v1/exchangerate/{crypto2}/{crypto}'
    headers = {'X-CoinAPI-Key' : APIKEY}
    response = requests.get(url, 
                            headers=headers)
    r = response.json()
    rate = r["rate"]
    rate = float(rate)
    cambio = q/rate  
    return cambio