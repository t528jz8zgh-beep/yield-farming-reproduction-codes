
import math
import numpy as np
import matplotlib.pyplot as plt


def buy_eth_with_usdt(x_usdt, y_eth, dx_usdt_in, fee=0.05):
    """Trader spends dx_usdt_in USDT to buy ETH.
    Pool: (x_usdt, y_eth) -> (x_usdt + dx, y_eth - dy_out)
    """
    if dx_usdt_in <= 0:
        return x_usdt, y_eth
    k = x_usdt * y_eth
    dy_no_fee = y_eth - k / (x_usdt + dx_usdt_in)     
    dy_out = (1.0 - fee) * dy_no_fee                 
    return x_usdt + dx_usdt_in, y_eth - dy_out

def sell_eth_for_usdt(x_usdt, y_eth, dy_eth_in, fee=0.05):
    """Trader sells dy_eth_in ETH to receive USDT.
    Pool: (x_usdt, y_eth) -> (x_usdt - dx_out, y_eth + dy)
    """
    if dy_eth_in <= 0:
        return x_usdt, y_eth
    k = x_usdt * y_eth
    dx_no_fee = x_usdt - k / (y_eth + dy_eth_in)     
    dx_out = (1.0 - fee) * dx_no_fee                
    return x_usdt - dx_out, y_eth + dy_eth_in

def simulate_fig5c(
    days=350,
    total_buy_usdt=50.0,
    total_sell_usdt=50.0,
    fee=0.05,
    reward_per_day=0.01,    
    lp_share=0.01,          
    reward_token_price=0.0,  
    p0=1.0                  
):

    x = 50.0
    y = x / p0

    buy_per_day = total_buy_usdt / days
    sell_per_day_usdt = total_sell_usdt / days

    reward_tokens = 0.0
    W = []

    for t in range(days + 1):
        pool_value = 2.0 * x
        W_t = lp_share * pool_value + reward_tokens * reward_token_price
        W.append(W_t)

        if t == days:
            break

        reward_tokens += lp_share * reward_per_day

        x, y = buy_eth_with_usdt(x, y, buy_per_day, fee=fee)

        p = x / y
        dy_in = sell_per_day_usdt / p
        x, y = sell_eth_for_usdt(x, y, dy_in, fee=fee)

    return np.array(W)

def main():
    days = 350
    volume_scenarios = [
        (0, 0),
        (45, 55),
        (50, 50),
        (55, 45),
    ]
    reward_prices = [0, 1, 2]

    for rp in reward_prices:
        plt.figure()
        for (b, s) in volume_scenarios:
            W = simulate_fig5c(days=days, total_buy_usdt=b, total_sell_usdt=s, reward_token_price=rp)
            plt.plot(range(days + 1), W, label=f"Volume (buy,sell)=({b},{s})")
        plt.title(f"Figure 5(c) replication — Reward token price = {rp} USDT")
        plt.xlabel("Day")
        plt.ylabel("W_t (USDT)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    plt.savefig("Wt_real_6months.png", dpi=200)
print("Saved plot: Wt_real_6months.png")

if __name__ == "__main__":
    main()