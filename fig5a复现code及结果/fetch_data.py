import requests
import json
from datetime import datetime, timedelta


def fetch_aave_usdt_data():
    url = "https://yields.llama.fi/pools"
    resp = requests.get(url)
    pools = resp.json()['data']
    

    aave_usdt = None
    for p in pools:
        if p.get('project') == 'aave-v3' and p.get('chain') == 'Ethereum' and 'USDT' in p.get('symbol', ''):
            aave_usdt = p
            print(f"Found: {p['symbol']} - Pool: {p['pool']}")
            break
    
    if not aave_usdt:
        print("Searching all USDT pools on Ethereum...")
        for p in pools:
            if p.get('chain') == 'Ethereum' and 'USDT' in p.get('symbol', '') and 'aave' in p.get('project', '').lower():
                print(f"  {p['project']}: {p['symbol']} - {p['pool']}")
    
    return aave_usdt

def fetch_pool_history(pool_id):
    url = f"https://yields.llama.fi/chart/{pool_id}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()['data']
    return None


def fetch_lend_borrow():
    url = "https://yields.llama.fi/lendBorrow"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
   
        for item in data:
            if 'aave' in item.get('project', '').lower() and item.get('chain') == 'Ethereum':
                if 'USDT' in item.get('symbol', ''):
                    print(f"Lend/Borrow: {item}")
    return resp.json() if resp.status_code == 200 else None

result = fetch_aave_usdt_data()
if result:
    print(f"\nPool ID: {result['pool']}")
    print(f"Current APY: {result.get('apy', 'N/A')}%")
    print(f"TVL: ${result.get('tvlUsd', 0):,.0f}")
    

    history = fetch_pool_history(result['pool'])
    if history:
        print(f"\nHistorical data points: {len(history)}")

        with open('aave_usdt_history.json', 'w') as f:
            json.dump(history, f, indent=2)
        print("Data saved to aave_usdt_history.json")
        

        for h in history[-5:]:
            print(f"  {h['timestamp'][:10]}: APY={h.get('apy', 0):.2f}%, TVL=${h.get('tvlUsd', 0):,.0f}")

