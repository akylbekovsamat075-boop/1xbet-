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
        Single iteration of the bot logic.
        """
        # 1. Fetch historical data
        df = self.bridge.get_historical_data(symbol, count=500)
        if df is None or df.empty:
            print("Failed to fetch data")
            return

        # 2. Apply Technical Indicators
        df = self.strategies.apply_indicators(df)

        # 3. Train AI if not trained (Self-Learning)
        if not self.ai_predictor.is_trained:
            print("Training AI model...")
            self.ai_predictor.train(df)

        # 4. Generate Strategy Signals
        df = self.strategies.generate_signals(df)
        last_row = df.iloc[-1:]

        strategy_signal = last_row['signal'].values[0]

        # 5. Get AI Prediction
        ai_signal = self.ai_predictor.predict(last_row)

        # 6. Final Decision Logic (Combining Technical + AI)
        final_decision = "HOLD"
        if strategy_signal == 1 and ai_signal == 1:
            final_decision = "BUY"
        elif strategy_signal == -1 and ai_signal == 0:
            final_decision = "SELL"

        print(f"Decision for {symbol}: {final_decision} (Strategy: {strategy_signal}, AI: {ai_signal})")

        # 7. Execute Trade
        if final_decision == "BUY":
            self.bridge.execute_buy(symbol)
        elif final_decision == "SELL":
            self.bridge.execute_sell(symbol)

    def start(self, symbol="EURUSD", interval=60):
        self.is_running = True
        print(f"Starting bot for {symbol}...")
        while self.is_running:
            try:
                self.run_once(symbol)
            except Exception as e:
                print(f"Error in loop: {e}")
            time.sleep(interval)

    def stop(self):
        self.is_running = False
