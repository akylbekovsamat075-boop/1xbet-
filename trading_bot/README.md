# Professional AI Trading Bot for XM

This project is a sophisticated trading bot designed to work with the XM broker via the MetaTrader 5 (MT5) platform. It combines professional technical indicators with a self-learning AI model to generate high-accuracy trading signals.

## Features
- **Technical Analysis**: Uses EMA, RSI, MACD, and Bollinger Bands.
- **Self-Learning AI**: Employs a Random Forest model that trains itself on historical data to predict price movements.
- **XM Integration**: Direct bridge to MetaTrader 5 for real-time execution.
- **Risk Management**: Designed with professional trading standards.

## Project Structure
- `bot_core.py`: The main logic loop.
- `xm_bridge.py`: Connection layer for XM/MT5.
- `strategies/technical.py`: Technical indicator implementations.
- `models/trainer.py`: AI training and prediction logic.
- `tests/`: Automated tests for all components.

## How to Use
1. Install requirements: `pip install -r requirements.txt`
2. Ensure MetaTrader 5 is installed and running on your Windows machine (or via Wine on Linux).
3. Update your credentials in a script or environment variables.
4. Run the bot.

## Disclaimer
Trading involves risk. This bot is for educational purposes.
