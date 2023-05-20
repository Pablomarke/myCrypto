import requests
from key import APIKEY



def valorCrypto(crypto):
    
    url = f'https://rest.coinapi.io/v1/exchangerate/{crypto}/EUR'
    headers = {'X-CoinAPI-Key' : APIKEY}
    response = requests.get(url, headers=headers)
    r = response.json()
    rate = r["rate"]
    return rate

print(valorCrypto("BTC"))

def comprarCrypto(eur, crypto):
    rate = valorCrypto(crypto)
    total = eur / rate
    return total

print("valor",comprarCrypto(25105, "BTC") )

def tradeoCrypto(q, crypto1, crypto2):
    
    url = f'https://rest.coinapi.io/v1/exchangerate/{crypto1}/{crypto2}'
    headers = {'X-CoinAPI-Key' : APIKEY}
    response = requests.get(url, headers=headers)
    r = response.json()
    rate = r["rate"]
    cambio = int(rate)*q  
    return cambio






