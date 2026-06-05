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
            print("[BRIDGE] MetaTrader5 library not found. Running in MOCK mode (SIMULATION).")
            self.connected = True
            return True

        print(f"[BRIDGE] Initializing MetaTrader5...")
        if not mt5.initialize():
            error_code = mt5.last_error()
            print(f"[BRIDGE] mt5.initialize() failed. Error code: {error_code}")
            return False

        if self.login:
            print(f"[BRIDGE] Attempting to login to XM server: {self.server}...")
            authorized = mt5.login(int(self.login), password=self.password, server=self.server)
            if not authorized:
                error_code = mt5.last_error()
                print(f"[BRIDGE] Failed to authorize at XM. Error code: {error_code}")
                return False
            print("[BRIDGE] Login successful!")

        self.connected = True
        return True

    def get_historical_data(self, symbol, count=500, timeframe="H1"):
        if mt5 is None:
            # Mock data generation
            dates = pd.date_range(end=pd.Timestamp.now(), periods=count, freq='h')
            df = pd.DataFrame({
                'time': dates,
                'open': np.random.uniform(1.08, 1.10, count),
                'high': np.random.uniform(1.10, 1.12, count),
                'low': np.random.uniform(1.06, 1.08, count),
                'close': np.random.uniform(1.08, 1.10, count),
                'tick_volume': np.random.randint(100, 1000, count)
            })
            return df

        # Map timeframe
        tf_map = {"M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5, "H1": mt5.TIMEFRAME_H1, "D1": mt5.TIMEFRAME_D1}
        mt5_tf = tf_map.get(timeframe, mt5.TIMEFRAME_H1)

        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 0, count)
        if rates is None:
            error = mt5.last_error()
            print(f"[BRIDGE] Failed to fetch data for {symbol}. Error: {error}")
            return None

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def execute_buy(self, symbol, volume=0.1):
        print(f"[TRADE] Executing BUY for {symbol} volume={volume}")
        if mt5 is None: return True

        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"[TRADE] {symbol} not found")
            return False

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).ask,
            "magic": 123456,
            "comment": "AI Bot Buy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"[TRADE] Order failed: {result.retcode}")
        else:
            print("[TRADE] Order executed successfully!")
        return result

    def execute_sell(self, symbol, volume=0.1):
        print(f"[TRADE] Executing SELL for {symbol} volume={volume}")
        if mt5 is None: return True

        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"[TRADE] {symbol} not found")
            return False

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid,
            "magic": 123456,
            "comment": "AI Bot Sell",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"[TRADE] Order failed: {result.retcode}")
        else:
            print("[TRADE] Order executed successfully!")
        return result

    def disconnect(self):
        if mt5:
            mt5.shutdown()
