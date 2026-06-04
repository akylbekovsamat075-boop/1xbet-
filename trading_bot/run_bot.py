import sys
import os

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xm_bridge import XMBridge
from bot_core import TradingBot

def run_trading_bot():
    print("==========================================")
    print("   AI TRADING BOT FOR XM / METATRADER 5   ")
    print("==========================================")

    # Initialize the bridge to XM
    # To use real account, pass: login=12345, password="your_password", server="XMGlobal-Real"
    bridge = XMBridge()

    print("[1/3] Connecting to XM/MT5...")
    if bridge.connect():
        print("[2/3] Connection successful!")
        bot = TradingBot(bridge)

        # You can change the symbol and interval here
        symbol = "EURUSD"
        interval = 60 # seconds

        print(f"[3/3] Starting trading loop for {symbol}...")
        print("Press Ctrl+C to stop.")

        try:
            # For demonstration, we run once.
            # In production, use bot.start(symbol, interval)
            bot.run_once(symbol)

            print("\nDemo run completed successfully.")
            print("To run continuously, edit run_bot.py and uncomment 'bot.start()'.")

        except KeyboardInterrupt:
            print("\nBot stopped by user.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
        finally:
            bridge.disconnect()
    else:
        print("[-] Error: Could not connect to MetaTrader 5.")
        print("Make sure MT5 is installed and 'Algo Trading' is enabled.")

if __name__ == "__main__":
    run_trading_bot()
