import csv
import time
from pycoingecko import CoinGeckoAPI
from defillama import DefiLlama
llama = DefiLlama()
cg = CoinGeckoAPI()
coin_gecko_coins_market = []

def get_interested_gecko_ids(category='Decentralized Exchange Token (DEX)', stopped_coin=''):
    file_name='dexes.csv'
    
    f = open(file_name, 'a')
    writer = csv.writer(f)
    tracker = 0

    try: 
        for coin in coin_gecko_coins_market:
            if tracker == 0 and coin['id'] != stopped_coin:
                continue
            tracker = 1
            stopped_coin = coin['id']
            coin_data = cg.get_coin_by_id(id=coin['id'])
            print(coin['id'])
            if category in coin_data['categories']:
                writer.writerow([coin['id']])
    except:
        f.close()
        return stopped_coin

    f.close()
    stopped_coin = "end"
    return stopped_coin

if __name__ == "__main__":
    stopped_coin = "gold-poker"
    while stopped_coin != "end":
        try:
            coin_gecko_coins_market = cg.get_coins_list(vs_currency="usd")
            stopped_coin = get_interested_gecko_ids(stopped_coin)
        except:
            time.sleep(30)
    print(stopped_coin)
