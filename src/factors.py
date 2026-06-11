# src/factors.py
import pandas as pd
import numpy as np

class FactorCalculator:
    """多因子计算器 - 可以直接复制使用"""

    def __init__(self, price_data):
        """
        初始化
        price_data: dict, key是股票代码, value是该股票的DataFrame(必须包含 'date', 'close')
        """
        self.price_data = price_data

    def calculate_momentum(self, df, lookback=20):
        """动量因子：过去N天收益率"""
        return df['close'].pct_change(lookback)

    def calculate_volatility(self, df, lookback=20):
        """低波动因子：历史波动率的倒数"""
        returns = df['close'].pct_change()
        volatility = returns.rolling(lookback).std()
        # 用倒数，波动越小得分越高。加一个小数防止除以0
        return 1 / (volatility + 1e-8)

    def calculate_all_factors(self):
        """为所有股票计算多个因子"""
        all_factors = []
        for code, df in self.price_data.items():
            temp_df = pd.DataFrame({
                'date': df['date'],
                'stock_code': code,
                'momentum': self.calculate_momentum(df),
                'low_volatility': self.calculate_volatility(df)
            })
            temp_df['market_cap'] = df['market_cap'] if 'market_cap' in df.columns else np.nan
            temp_df['roe'] = df['roe'] if 'roe' in df.columns else np.nan
            all_factors.append(temp_df)

        factor_df = pd.concat(all_factors, ignore_index=True)
        return factor_df

    def normalize_factors(self, factor_df):
        """使用百分位排名法标准化因子"""
        factor_cols = ['momentum', 'low_volatility', 'market_cap', 'roe']
        for col in factor_cols:
            # 按日期分组，将每个因子转换为0到1之间的排名分
            factor_df[f'{col}_normalized'] = factor_df.groupby('date')[col].rank(pct=True)
        return factor_df

    def combine_factors(self, normalized_df):
        """等权重合成最终的综合得分"""
        normalized_df['composite_score'] = (
            normalized_df['momentum_normalized'] * 0.5 + 
            normalized_df['low_volatility_normalized'] * 0.5
        )
        return normalized_df