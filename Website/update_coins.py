from posixpath import split
from Website import db
from Website.Models import Market,User
import json
from requests import Request, Session

def get_price(slug,coin_id): # this function return price and change
    coin_id = str(coin_id)
    # calling the API
    url_for_price = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {'slug':slug}
    headers = { 'Accepts': 'application/json',  # return format of json
        'X-CMC_PRO_API_KEY': '74288599-b578-4f5a-8f09-48409de7b08f' }
    session = Session()
    session.headers.update(headers)

    response = session.get(url_for_price , params=parameters)
    data = json.loads(response.text)

    # getting the info
    coin_price = data['data'][coin_id]['quote']['USD']['price']

    # getting the coin changes
    coin_1 = data['data'][coin_id]['quote']['USD']['percent_change_1h']
    coin_24 = data['data'][coin_id]['quote']['USD']['percent_change_24h']
    coin_7 = data['data'][coin_id]['quote']['USD']['percent_change_7d']
    coin_30 = data['data'][coin_id]['quote']['USD']['percent_change_30d']
    # total supply
    coin_total = data['data'][coin_id]['max_supply']
    coin_price = view(coin_price)
    coin_1 = view(coin_1)
    coin_24 = view(coin_24)
    coin_7 = view(coin_7)
    coin_30 = view(coin_30)

    print(f"Price --> {coin_price}")
    print(f"Changes -->[{coin_1} ,{coin_24} ,{coin_7}, {coin_30}]")
    print(f"Supply --> {coin_total}")
    A = [coin_price , coin_1 , coin_24 , coin_7, coin_30]
    return A

def view(text):
    text = str(text)
    x,y = map(str,text.split("."))
    z = y[0:2]
    ans = x+'.'+ z
    return ans

def get_coin():
    coin = Market.query.all()
    for i in coin:
        coin_slug = i.coin_slug
        coin_id = i.coin_id
        A = get_price(coin_slug,coin_id)
        i.coin_price = A[0]
        i.coin_1 = A[1]
        i.coin_24 = A[2]
        i.coin_7 = A[3]
        i.coin_30 = A[4]
        db.session.commit()
        



def update_coin():
    get_coin()