from requests import Request, Session
import json
import pprint as p
from Website import db
from Website.Models import Market

def add_coin(slug, coin_id):

    def get_price(slug, coin_id):  # this function return price and change
        coin_id = str(coin_id)
        # calling the API
        url_for_price = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        parameters = {'slug': slug}
        headers = {'Accepts': 'application/json',  # return format of json
                   'X-CMC_PRO_API_KEY': '74288599-b578-4f5a-8f09-48409de7b08f'}
        session = Session()
        session.headers.update(headers)

        response = session.get(url_for_price, params=parameters)
        data = json.loads(response.text)

        # p.pprint(data['data'][coin_id]['quote'])
        # getting the info
        coin_price = data['data'][coin_id]['quote']['USD']['price']

        # getting the coin changes
        coin_1 = data['data'][coin_id]['quote']['USD']['percent_change_1h']
        coin_24 = data['data'][coin_id]['quote']['USD']['percent_change_24h']
        coin_7 = data['data'][coin_id]['quote']['USD']['percent_change_7d']
        coin_30 = data['data'][coin_id]['quote']['USD']['percent_change_30d']
        # total supply
        coin_total = data['data'][coin_id]['max_supply']
        if not coin_total:
            coin_total = 1000000

        print(f"Price --> {coin_price}")
        print(f"Changes -->[{coin_1} ,{coin_24} ,{coin_7}, {coin_30}]")
        print(f"Supply --> {coin_total}")
        A = [coin_id, slug, coin_price, coin_total,
             coin_1, coin_24, coin_7, coin_30]
        return A

    def get_info(slug, coin_id):

        coin_id = str(coin_id)

        # calling the API
        url_for_info = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
        parameters = {'slug': slug}
        headers = {'Accepts': 'application/json',  # return format of json
                   'X-CMC_PRO_API_KEY': '74288599-b578-4f5a-8f09-48409de7b08f'}
        session = Session()
        session.headers.update(headers)
        response = session.get(url_for_info, params=parameters)
        data = json.loads(response.text)

        # getting the info
        coin_info = data['data'][coin_id]['description']
        coin_logo = data['data'][coin_id]['logo']
        coin_website = data['data'][coin_id]['urls']['website'][0]
        coin_paper = data['data'][coin_id]['urls']['technical_doc']
        if coin_paper:
            coin_paper = coin_paper = data['data'][coin_id]['urls']['technical_doc'][0]
        else:
            coin_paper = 'Not Available'
        coin_name = data['data'][coin_id]['name']
        coin_name = data['data'][coin_id]['name']

        print(f"Description --> {coin_info}")
        print(
            f"Logo-->{coin_logo} Website --> {coin_website} Paper --> {coin_paper}")
        B = [coin_info, coin_logo, coin_paper, coin_website , coin_name]
        return B

    # calling the price and info function
    A = get_price(slug, coin_id)
    B = get_info(slug, coin_id)

    def db_add_coins(A, B):
        #A = [coin_id, slug, coin_price, coin_total, coin_1, coin_24, coin_7, coin_30]
        #B = [coin_info, coin_logo, coin_paper, coin_website]
        coin = Market(
            coin_id=A[0], coin_slug=A[1], coin_price=A[2], coin_total=A[3], coin_1=A[4],
            coin_24=A[5], coin_7=A[6], coin_30=A[7], coin_info=B[0], coin_logo=B[1], coin_paper=B[2],
            coin_website=B[3], coin_name = B[4])
        db.session.add(coin)
        db.session.commit()
    db_add_coins(A, B)


def add_coins(symbol):  # gets the symbol arguement which is used to collect the id and slug of the coin

    # calling the API for collecting slug and id
    url_for_getting_slug_and_id = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    param = {'symbol': symbol}
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': '74288599-b578-4f5a-8f09-48409de7b08f'}
    session = Session()
    session.headers.update(headers)
    response_id = session.get(url_for_getting_slug_and_id, params=param)
    data_id = json.loads(response_id.text)

    # getting the desired info
    coin_id = data_id['data'][0]['id']
    coin_slug = data_id['data'][0]['slug']
    add_coin(coin_slug, coin_id)


def add_coins_list():  # adding the coins data using the symbols of the coins.
    symbol_list = [ 'DOT', 'FTM', 'SAND', 'MANA']
    for i in symbol_list:
        add_coins(i)


# calling the add function
# add_coins_list()
