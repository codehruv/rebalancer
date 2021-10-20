import csv
import time

from pycoingecko import CoinGeckoAPI
from defillama import DefiLlama

llama = DefiLlama()
cg = CoinGeckoAPI()

output_list_2d = []
with open('output.txt') as f:
    reader = csv.reader(f)
    output_list_2d = list(reader)

fields = []

for field in output_list_2d:
    fields.extend(field)


def write_coin_data_to_file(stopped_id, gecko_ids=[], file_to_write_to='coin_data.csv'):
    f = open(file_to_write_to, 'a')
    writer = csv.writer(f)

    tracker = 0

    try:
        for gecko_id in gecko_ids:
            if tracker == 0 and gecko_id != stopped_id:
                continue
            tracker = 1
            stopped_id = gecko_id

            coin_data = cg.get_coin_by_id(id=gecko_id)
            coin_price = cg.get_price(ids=gecko_id, vs_currencies="usd")
            llama_data = llama.get_protocol(name=coin_data['id'])

            coin_data.pop('localization')
            coin_data.pop('image')
            coin_data['description'] = coin_data['description']['en']
            coin_data['platforms'] = list(coin_data['platforms'].keys())

            nested_keys = ['market_data', 'community_data', 'developer_data', 'public_interest_stats']
            for nested_key in nested_keys:
                for key in coin_data[nested_key].keys():
                    if isinstance(coin_data[nested_key][key], dict) and 'usd' in coin_data[nested_key][key].keys():
                        coin_data[key + '_usd'] = coin_data[nested_key][key]['usd']
                        continue
                    coin_data[key] = coin_data[nested_key][key]
                coin_data.pop(nested_key)

            coin_data['number_of_listings'] = len(coin_data['tickers'])
            coin_data.pop('tickers')

            coin_data['audits'] = llama_data['audits'] if 'audits' in llama_data.keys() else "0"
            coin_data['audit_links'] = llama_data['audit_links'] if 'audit_links' in llama_data.keys() else ""
            coin_data['oracles'] = llama_data['oracles'] if 'oracles' in llama_data.keys() else ""
            coin_data['price'] = coin_price[gecko_id]['usd']
            
            if len(coin_data.keys()) < 90 or isinstance(coin_data['market_cap_rank'], dict):
                print(coin_data['id'])
            else:
                writer.writerow(coin_data.values())
    except:
        f.close()
        return stopped_id
    
    f.close()
    return "end"


# TODO add code for getting correct number of listings using page parameter in tickers API
# TODO use price api with market_cap included to get 24h volume
"""if gecko_id == gecko_ids[0]:
                header = coin_data.keys()
                writer.writerow(header)"""

if __name__ == "__main__":
    dexes_list_2d = []
    with open('dexes.csv') as f:
        reader = csv.reader(f)
        dexes_list_2d = list(reader)
    
    dexes_list = []

    for dex in dexes_list_2d:
        dexes_list.extend(dex)

    dexes_list = ['bancor']
    stopped_coin = "bancor"
    while stopped_coin != "end":
        try:
            stopped_coin = write_coin_data_to_file(stopped_coin, dexes_list, 'dexes_data.csv')
        except:
            time.sleep(30)
    