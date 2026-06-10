# src/backtest.py
import pandas as pd
import numpy as np
from .factors import FactorCalculator

class MultiFactorBacktest:
    """多因子选股回测"""

    def __init__(self, price_data, start_date, end_date, top_n=3):
        self.price_data = price_data
        self.start_date = start_date
        self.end_date = end_date
        self.top_n = top_n

    def run_backtest(self, rebalance_freq=20):
        """执行回测"""
        # 1. 计算因子
        factor_calc = FactorCalculator(self.price_data)
        raw_factors = factor_calc.calculate_all_factors()
        normalized = factor_calc.normalize_factors(raw_factors)
        combined = factor_calc.combine_factors(normalized)

        # 2. 获取所有交易日（修复日期类型问题）
        all_dates = sorted(combined['date'].unique())
        start_ts = pd.to_datetime(self.start_date)
        end_ts = pd.to_datetime(self.end_date)
        start_ts = pd.to_datetime(self.start_date)
        end_ts = pd.to_datetime(self.end_date)
        all_dates = [d for d in all_dates if start_ts <= d <= end_ts]
        
        rebalance_dates = all_dates[::rebalance_freq]

        portfolio_returns = []
        
        for i, trade_date in enumerate(rebalance_dates):
            today_factors = combined[combined['date'] == trade_date]
            selected = today_factors.nlargest(self.top_n, 'composite_score')['stock_code'].tolist()
            
            if i < len(rebalance_dates) - 1:
                next_date = rebalance_dates[i+1]
            else:
                next_date = all_dates[-1]
            
            period_ret = self._calc_period_return(selected, trade_date, next_date)
            if period_ret is not None:
                portfolio_returns.append(period_ret)

        if portfolio_returns:
            total_return = (1 + pd.Series(portfolio_returns)).prod() - 1
            return {'total_return': total_return, 'daily_returns': portfolio_returns}
        return {'total_return': 0, 'daily_returns': []}

    def _calc_period_return(self, stocks, start_date, end_date):
        """计算指定区间内，持仓股票的平均收益率"""
        stock_returns = []
        for stock in stocks:
            df = self.price_data.get(stock)
            if df is not None:
                start_row = df[df['date'] == start_date]
                end_row = df[df['date'] == end_date]
                if not start_row.empty and not end_row.empty:
                    ret = (end_row['close'].values[0] - start_row['close'].values[0]) / start_row['close'].values[0]
                    stock_returns.append(ret)
        if stock_returns:
            return np.mean(stock_returns)
        return None