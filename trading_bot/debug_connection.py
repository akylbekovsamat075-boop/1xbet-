import MetaTrader5 as mt5
import sys

def debug_xm():
    print("--- Проверка подключения к XM ---")
    if not mt5.initialize():
        print(f"Ошибка инициализации: {mt5.last_error()}")
        return

    print("MetaTrader 5 успешно инициализирован.")

    # Информация о терминале
    terminal_info = mt5.terminal_info()
    if terminal_info:
        print(f"Подключено к терминалу: {terminal_info.company}")

    # Проверка символа
    symbol = "EURUSD"
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Символ {symbol} не найден. Проверьте 'Обзор рынка'.")
    else:
        print(f"Символ {symbol} найден. Текущая цена Ask: {mt5.symbol_info_tick(symbol).ask}")

    mt5.shutdown()

if __name__ == "__main__":
    try:
        import MetaTrader5
        debug_xm()
    except ImportError:
        print("Библиотека MetaTrader5 не установлена. На Linux она не будет работать напрямую.")
