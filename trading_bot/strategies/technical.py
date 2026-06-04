import pandas as pd
import pandas_ta as ta

class TechnicalStrategies:
    @staticmethod
    def apply_indicators(df):
        """
        Applies standard professional indicators to the dataframe.
        Expected columns in df: 'open', 'high', 'low', 'close', 'volume'
        """
        # Ensure we have enough data
        if len(df) < 50:
            return df

        # EMA 9 and 21 (Common for short-term trend)
        df['EMA_9'] = ta.ema(df['close'], length=9)
        df['EMA_21'] = ta.ema(df['close'], length=21)

        # RSI (Momentum)
        df['RSI'] = ta.rsi(df['close'], length=14)

        # MACD (Trend and Momentum)
        macd = ta.macd(df['close'])
        df = pd.concat([df, macd], axis=1)

        # Bollinger Bands (Volatility)
        bbands = ta.bbands(df['close'], length=20, std=2)
        df = pd.concat([df, bbands], axis=1)

        return df

    @staticmethod
    def generate_signals(df):
        """
        Generates basic signals based on technical indicators.
        1: Buy, -1: Sell, 0: Hold
        """
        df['signal'] = 0

        # Simple Example Strategy: EMA Crossover + RSI filter
        # Buy when EMA 9 crosses above EMA 21 and RSI < 70
        buy_cond = (df['EMA_9'] > df['EMA_21']) & (df['EMA_9'].shift(1) <= df['EMA_21'].shift(1)) & (df['RSI'] < 70)
        # Sell when EMA 9 crosses below EMA 21 and RSI > 30
        sell_cond = (df['EMA_9'] < df['EMA_21']) & (df['EMA_9'].shift(1) >= df['EMA_21'].shift(1)) & (df['RSI'] > 30)

        df.loc[buy_cond, 'signal'] = 1
        df.loc[sell_cond, 'signal'] = -1

        return df
