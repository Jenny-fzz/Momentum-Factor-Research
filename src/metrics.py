import pandas as pd
from scipy.stats import spearmanr

def compute_ic(df, factor_col="momentum", forward_return_col="future_return_5d"):
    """
    计算每日 IC
    """
    ic_list = []
    dates = sorted(df["trade_date"].unique())
    for date in dates:
        temp = df[df["trade_date"]==date].dropna(subset=[factor_col, forward_return_col])
        if len(temp)<5:
            continue
        ic, _ = spearmanr(temp[factor_col], temp[forward_return_col])
        ic_list.append({"date": date, "IC": ic})
    return pd.DataFrame(ic_list)