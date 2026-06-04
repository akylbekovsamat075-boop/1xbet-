import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

class AISignalPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def prepare_data(self, df):
        """
        Prepares features and labels for training.
        Label: 1 if next period price is higher, 0 otherwise.
        """
        # Select features (indicators)
        features = ['EMA_9', 'EMA_21', 'RSI', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9']
        # Filter features that exist in df
        features = [f for f in features if f in df.columns]

        if not features:
            return None, None

        data = df[features].copy()
        # Drop rows with NaN from indicators
        data = data.dropna()

        # Target: Price goes up in the next candle
        target = (df['close'].shift(-1) > df['close']).astype(int)
        target = target.loc[data.index]

        # Remove the last row since we don't have a label for it
        return data.iloc[:-1], target.iloc[:-1]

    def train(self, df):
        X, y = self.prepare_data(df)
        if X is None or len(X) < 100:
            return False

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        return True

    def predict(self, current_features):
        """
        Predicts if price will go up (1) or down (0).
        current_features: a single row DataFrame or series with indicators.
        """
        if not self.is_trained:
            return None

        # Ensure only expected features are used
        features = ['EMA_9', 'EMA_21', 'RSI', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9']
        # Filter existing features
        features = [f for f in features if f in current_features.columns]

        prediction = self.model.predict(current_features[features])
        return prediction[0]
