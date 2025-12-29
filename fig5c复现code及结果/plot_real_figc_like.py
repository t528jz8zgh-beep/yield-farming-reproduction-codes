import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def impermanent_loss_multiplier(r):
    r = np.maximum(r, 1e-12)
    return (2 * np.sqrt(r)) / (1 + r)

def compute_real_Wt_from_ohlcv(
    df,
    initial_value=1.0,
    lp_share=0.0001,
    fee_rate=0.003,
    reward_per_day=0.0,         
    reward_token_price=0.0,
    volume_scale=1.0
):
    df = df.copy()
    df["datetime_utc"] = pd.to_datetime(df["datetime_utc"], utc=True)
    df = df.sort_values("datetime_utc").reset_index(drop=True)

    p0 = df.loc[0, "close"]
    r = df["close"] / p0
    lp_value_no_fee = initial_value * impermanent_loss_multiplier(r)

    fee_income = fee_rate * (df["volume"] * volume_scale) * lp_share
    cum_fee_income = fee_income.cumsum()

    t = np.arange(len(df))
    reward_tokens = lp_share * reward_per_day * t
    reward_value = reward_tokens * reward_token_price

    W_t = lp_value_no_fee + cum_fee_income + reward_value
    return df["datetime_utc"], W_t

if __name__ == "__main__":
    csv_name = "ohlcv_eth_0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852_day_180d.csv"
    csv_path = Path(__file__).with_name(csv_name)
    df = pd.read_csv(csv_path)

    initial_value = 1.0
    lp_share = 0.0001        
    fee_rate = 0.003         
    reward_per_day = 0.0    

    reward_prices = [0, 1, 2]               
    volume_scales = [0.0, 0.7, 1.0, 1.3]     
    labels = [f"volume x{vs:g}" for vs in volume_scales]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)

    for ax, rp in zip(axes, reward_prices):
        for vs, lab in zip(volume_scales, labels):
            dt, W = compute_real_Wt_from_ohlcv(
                df,
                initial_value=initial_value,
                lp_share=lp_share,
                fee_rate=fee_rate,
                reward_per_day=reward_per_day,
                reward_token_price=rp,
                volume_scale=vs
            )
            ax.plot(dt, W, label=lab)

        ax.set_title(f"Real-data analogue — Reward token price = {rp} USDT")
        ax.set_xlabel("Date (UTC)")
        ax.grid(True, alpha=0.3)

    axes[0].set_ylabel("W_t (USDT)")
    axes[0].legend(title="Scenarios", fontsize=9)

    plt.tight_layout()

    
    out_png = Path(__file__).with_name("figc_realdata_analogue.png")
    plt.savefig(out_png, dpi=200)
    print("Saved:", out_png)

    plt.show()

