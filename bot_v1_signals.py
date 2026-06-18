#!/usr/bin/env python
# coding: utf-8

# In[1]:


# bot_v1_signals
# Выдача сигналов без торговли
import pandas as pd
import os
import logging
import time
from dotenv import load_dotenv
from pybit.unified_trading import HTTP
from config import STRATEGY_PARAMS, SYMBOL, TIMEFRAME
from strategy import generating_signals

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

# Настройка прокси
proxy_url = f"http://{os.getenv('PROXY_LOGIN')}:{os.getenv('PROXY_PASSWORD')}@{os.getenv('PROXY_HOST')}:{os.getenv('PROXY_PORT')}"
os.environ['HTTP_PROXY'] = proxy_url
os.environ['HTTPS_PROXY'] = proxy_url

# Настройка подключения к Байбит
session = HTTP(
    testnet=True,
    api_key=os.getenv('BYBIT_API_KEY'),
    api_secret=os.getenv('BYBIT_SECRET')
)
public_session = HTTP(testnet=True, timeout=30)

def fetch_klines(limit=200):
    klines = public_session.get_kline(
        category='spot',
        symbol = SYMBOL,
        interval = TIMEFRAME,
        limit = limit)
    ticker_df = pd.DataFrame(klines.get('result').get('list'), columns=['datetime', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    ticker_df['datetime'] = pd.to_datetime(ticker_df['datetime'].astype('int64'), unit='ms')
    ticker_df.set_index('datetime', inplace=True)
    ticker_df = ticker_df.astype('float64')
    ticker_df = ticker_df.sort_index()

    return ticker_df

def main():
    logger.info("🤖 Робот запущен (режим сигналов)")
    logger.info(f"Символ: {SYMBOL}")
    logger.info(f"Таймфрейм: {TIMEFRAME}")
    logger.info(f"Параметры: {STRATEGY_PARAMS}")
    logger.info("="*50)

    last_signal = None

    while True:
        try:
            df = fetch_klines(limit=200)
            signal, sl, tp = generating_signals(df, STRATEGY_PARAMS)
            if signal == 1 and last_signal != 1:
                logger.info(f"🟢 LONG сигнал! Цена: {df['close'].iloc[-1]:.2f}")
                last_signal = 1
            elif signal == -1 and last_signal != -1:
                logger.info(f"🔴 SHORT сигнал! Цена: {df['close'].iloc[-1]:.2f}")
                last_signal = -1

            time.sleep(60)

        except KeyboardInterrupt:
            logger.info("\n🛑 Робот остановлен")
            break
        except Exception as e:
            logger.info(f"❌ Ошибка: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()



# In[ ]:





# In[ ]:




