# src/fetch_data.py
import tushare as ts
import pandas as pd
from pathlib import Path

def get_fundamental_data():
    """获取所有股票的市值和ROE数据"""
    
    # 设置token（替换成你的）
    ts.set_token('16eb74c542f8d12a75d6efdda2f673f8d3acdc16ccb258b8d78b646c')
    pro = ts.pro_api()
    
    # 读取已有的股票列表
    data_dir = Path('./data')
    stock_codes = [f.stem for f in data_dir.glob('*.csv')]
    
    print(f"共有 {len(stock_codes)} 只股票")
    
    # 获取第一只股票测试
    code = stock_codes[0]
    print(f"\n测试获取 {code} 的数据...")
    
    # 获取市值
    df_mv = pro.daily_basic(
        ts_code=code, 
        start_date='20240101', 
        end_date='20241231', 
        fields='trade_date,total_mv'
    )
    
    # 获取ROE
    df_roe = pro.fina_indicator(
        ts_code=code, 
        start_date='20240101', 
        end_date='20241231',
        fields='end_date,roe'
    )
    
    print("\n市值数据：")
    print(df_mv.head())
    print("\nROE数据：")
    print(df_roe.head())
    
    return df_mv, df_roe

if __name__ == "__main__":
    get_fundamental_data()