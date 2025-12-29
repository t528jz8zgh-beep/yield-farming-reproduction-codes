import requests
import pandas as pd
from datetime import datetime, timezone


POOL_ADDRESS = "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852"
NETWORK = "eth"   
LIMIT = 180       

def fetch_ohlcv_geckoterminal(network, pool_address, timeframe="day", limit=180, aggregate=1):
    url = f"https://api.geckoterminal.com/api/v2/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}"
    params = {
        "aggregate": aggregate,
        "limit": limit,
        "currency": "usd",
        "token": "base"  
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()["data"]["attributes"]["ohlcv_list"]
  
    df = pd.DataFrame(data, columns=["ts", "open", "high", "low", "close", "volume"])
    df["datetime_utc"] = pd.to_datetime(df["ts"], unit="s", utc=True)
    df = df.sort_values("datetime_utc").reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = fetch_ohlcv_geckoterminal(NETWORK, POOL_ADDRESS, TIMEFRAME, LIMIT, aggregate=1)
    out = f"ohlcv_{NETWORK}_{POOL_ADDRESS}_{TIMEFRAME}_{LIMIT}d.csv"
    df.to_csv(out, index=False)
    print("Saved:", out)
    print(df.tail())