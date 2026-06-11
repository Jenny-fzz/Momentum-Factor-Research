# src/ma_backtest.py
import pandas as pd
import numpy as np

class MABacktest:
    """双均线回测"""
    
    def __init__(self, df, initial_capital=100000):
        self.df = df.copy()
        self.initial_capital = initial_capital
        self.results = None
    
    def run(self):
        """运行回测"""
        capital = self.initial_capital
        position = 0
        
        self.df['portfolio'] = 0.0
        self.df['holdings'] = 0.0
        self.df['cash'] = self.initial_capital
        
        for i, row in self.df.iterrows():
            if row['buy'] == 1 and capital > 0:
                position = capital / row['close']
                capital = 0
            elif row['sell'] == 1 and position > 0:
                capital = position * row['close']
                position = 0
            
            holdings = position * row['close']
            self.df.loc[i, 'holdings'] = holdings
            self.df.loc[i, 'cash'] = capital
            self.df.loc[i, 'portfolio'] = holdings + capital
        
        # 计算指标
        self.df['daily_return'] = self.df['portfolio'].pct_change()
        
        total_return = (self.df['portfolio'].iloc[-1] - self.initial_capital) / self.initial_capital
        
        # 最大回撤
        cummax = self.df['portfolio'].cummax()
        drawdown = (self.df['portfolio'] - cummax) / cummax
        max_drawdown = drawdown.min()
        
        # 年化收益
        days = len(self.df)
        years = days / 252
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 夏普比率
        risk_free = 0.03
        excess = self.df['daily_return'] - risk_free / 252
        sharpe = np.sqrt(252) * excess.mean() / excess.std() if excess.std() > 0 else 0
        
        self.results = {
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'final_value': self.df['portfolio'].iloc[-1],
            'trade_count': (self.df['buy'].sum() + self.df['sell'].sum())
        }
        
        return self.results, self.df