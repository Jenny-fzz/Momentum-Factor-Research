import pandas as pd
import glob
import os

def load_stock_data(data_path="../data"):
    files = glob.glob(os.path.join(data_path, "*.csv"))
    all_data = []
    for file in files:
        df = pd.read_csv(file)
        df["ts_code"] = os.path.basename(file).replace(".csv","")
        all_data.append(df)
    all_df = pd.concat(all_data, ignore_index=True)
    all_df = all_df.sort_values(["trade_date", "ts_code"]).reset_index(drop=True)
    return all_df