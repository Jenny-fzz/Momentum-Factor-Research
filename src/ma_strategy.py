import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DoubleMAStrategy:
    def __init__(self, df, fast=5, slow=20):
        self.df = df.copy()
        self.fast = fast
        self.slow = slow
    
    def backtest(self, initial_capital=100000):
        self.df['ma_fast'] = self.df['close'].rolling(self.fast).mean()
        self.df['ma_slow'] = self.df['close'].rolling(self.slow).mean()
        
        self.df['position'] = 0
        self.df.loc[self.df['ma_fast'] > self.df['ma_slow'], 'position'] = 1
        
        self.df['portfolio'] = initial_capital
        for i in range(1, len(self.df)):
            if self.df['position'].iloc[i] == 1:
                self.df.loc[i, 'portfolio'] = self.df['portfolio'].iloc[i-1] * self.df['close'].iloc[i] / self.df['close'].iloc[i-1]
            else:
                self.df.loc[i, 'portfolio'] = self.df['portfolio'].iloc[i-1]
        
        total_return = (self.df['portfolio'].iloc[-1] - initial_capital) / initial_capital
        return {'total_return': total_return}, self.df