from xm_bridge import XMBridge
from bot_core import TradingBot

def main():
    # Создаем мост к XM (по умолчанию включится MOCK режим если нет библиотеки MT5)
    bridge = XMBridge()

    if bridge.connect():
        bot = TradingBot(bridge)
        # Запускаем один цикл для теста
        print("--- Тестовый запуск бота ---")
        bot.run_once("EURUSD")
        print("--- Тестовый запуск завершен ---")

        # В реальной ситуации здесь был бы bot.start()
        # bot.start("EURUSD", interval=60)
    else:
        print("Не удалось подключиться к XM/MT5")

if __name__ == "__main__":
    main()
