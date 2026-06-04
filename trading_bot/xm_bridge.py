import pandas as pd
import numpy as np

try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None

class XMBridge:
    def __init__(self, login=None, password=None, server=None):
        self.login = login
        self.password = password
        self.server = server
        self.connected = False

    def connect(self):
        if mt5 is None:
            print("MetaTrader5 library not found. Running in MOCK mode.")
            self.connected = True
            return True

        if not mt5.initialize():
            print("mt5.initialize() failed")
            return False

        if self.login:
            authorized = mt5.login(self.login, password=self.password, server=self.server)
            if not authorized:
                print(f"Failed to authorize at XM server {self.server}")
                return False

        self.connected = True
        return True

    def get_historical_data(self, symbol, count=500, timeframe="H1"):
        if mt5 is None:
            # Mock data generation for testing
            dates = pd.date_range(end=pd.Timestamp.now(), periods=count, freq='h')
            df = pd.DataFrame({
                'time': dates,
                'open': np.random.uniform(1.08, 1.10, count),
                'high': np.random.uniform(1.08, 1.10, count),
                'low': np.random.uniform(1.08, 1.10, count),
                'close': np.random.uniform(1.08, 1.10, count),
                'tick_volume': np.random.randint(100, 1000, count)
            })
            return df

        # Map timeframe string to MT5 constant
        tf_map = {"M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5, "H1": mt5.TIMEFRAME_H1, "D1": mt5.TIMEFRAME_D1}
        mt5_tf = tf_map.get(timeframe, mt5.TIMEFRAME_H1)

        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 0, count)
        if rates is None:
            return None

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def execute_buy(self, symbol, volume=0.1):
        print(f"MT5: Executing BUY for {symbol} volume={volume}")
        if mt5 is None: return True

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).ask,
            "magic": 123456,
            "comment": "Bot trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return result

    def execute_sell(self, symbol, volume=0.1):
        print(f"MT5: Executing SELL for {symbol} volume={volume}")
        if mt5 is None: return True

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid,
            "magic": 123456,
            "comment": "Bot trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return result

    def disconnect(self):
        if mt5:
            mt5.shutdown()
