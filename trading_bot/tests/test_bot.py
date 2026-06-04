import pytest
import pandas as pd
import numpy as np
from strategies.technical import TechnicalStrategies
from models.trainer import AISignalPredictor
from xm_bridge import XMBridge

def test_technical_indicators():
    df = pd.DataFrame({
        'close': np.random.uniform(1.0, 1.1, 100),
        'open': np.random.uniform(1.0, 1.1, 100),
        'high': np.random.uniform(1.0, 1.1, 100),
        'low': np.random.uniform(1.0, 1.1, 100),
        'volume': np.random.randint(100, 1000, 100)
    })

    df_with_indicators = TechnicalStrategies.apply_indicators(df)
    assert 'EMA_9' in df_with_indicators.columns
    assert 'RSI' in df_with_indicators.columns
    assert 'MACD_12_26_9' in df_with_indicators.columns

def test_ai_trainer():
    df = pd.DataFrame({
        'close': np.random.uniform(1.0, 1.1, 200),
        'open': np.random.uniform(1.0, 1.1, 200),
        'high': np.random.uniform(1.0, 1.1, 200),
        'low': np.random.uniform(1.0, 1.1, 200),
        'volume': np.random.randint(100, 1000, 200)
    })
    df = TechnicalStrategies.apply_indicators(df)

    predictor = AISignalPredictor()
    success = predictor.train(df)
    assert success is True
    assert predictor.is_trained is True

    last_row = df.iloc[-1:]
    prediction = predictor.predict(last_row)
    assert prediction in [0, 1]

def test_xm_bridge_mock():
    bridge = XMBridge()
    bridge.connect()
    assert bridge.connected is True

    df = bridge.get_historical_data("EURUSD", count=50)
    assert len(df) == 50
    assert 'close' in df.columns
