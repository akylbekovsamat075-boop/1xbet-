import time
import pandas as pd
from strategies.technical import TechnicalStrategies
from models.trainer import AISignalPredictor

class TradingBot:
    def __init__(self, bridge):
        self.bridge = bridge
        self.strategies = TechnicalStrategies()
        self.ai_predictor = AISignalPredictor()
        self.is_running = False

    def run_once(self, symbol="EURUSD"):
        """
        Single iteration with detailed logging.
        """
        print(f"\n[BOT] --- Start iteration for {symbol} ---")

        # 1. Fetch historical data
        print(f"[BOT] Fetching data...")
        df = self.bridge.get_historical_data(symbol, count=500)
        if df is None or df.empty:
            print("[BOT] ERROR: No data received.")
            return

        # 2. Apply Technical Indicators
        print(f"[BOT] Calculating indicators...")
        df = self.strategies.apply_indicators(df)

        # 3. Train/Update AI model
        if not self.ai_predictor.is_trained:
            print("[BOT] AI model not trained. Starting training...")
            success = self.ai_predictor.train(df)
            if success:
                print("[BOT] AI model trained successfully.")
            else:
                print("[BOT] AI training failed (not enough data?)")

        # 4. Analyze current market state
        df = self.strategies.generate_signals(df)
        last_row = df.iloc[-1:]

        tech_signal = last_row['signal'].values[0]
        ai_signal = self.ai_predictor.predict(last_row)

        print(f"[BOT] Technical Signal: {'BUY' if tech_signal == 1 else 'SELL' if tech_signal == -1 else 'HOLD'}")
        print(f"[BOT] AI Prediction: {'UP' if ai_signal == 1 else 'DOWN' if ai_signal == 0 else 'UNKNOWN'}")

        # 5. Final Decision
        if tech_signal == 1 and ai_signal == 1:
            print("[BOT] CONFIRMED BUY: Technical and AI match.")
            self.bridge.execute_buy(symbol)
        elif tech_signal == -1 and ai_signal == 0:
            print("[BOT] CONFIRMED SELL: Technical and AI match.")
            self.bridge.execute_sell(symbol)
        else:
            print("[BOT] NO ACTION: Signals do not match or HOLD signal received.")

        print(f"[BOT] --- End iteration ---")

    def start(self, symbol="EURUSD", interval=60):
        self.is_running = True
        print(f"\n[SYSTEM] Trading bot started. Target: {symbol}, Interval: {interval}s")
        while self.is_running:
            try:
                self.run_once(symbol)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[SYSTEM] Critical error: {e}")
            time.sleep(interval)

    def stop(self):
        self.is_running = False
        print("[SYSTEM] Bot stopping...")
