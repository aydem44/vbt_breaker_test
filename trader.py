#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import logging
from dotenv import load_dotenv
from pybit.unified_trading import HTTP
from config import CATEGORY

load_dotenv()
logger = logging.getLogger(__name__)

proxy_host = os.getenv('PROXY_HOST')
proxy_port = os.getenv('PROXY_PORT')
proxy_login = os.getenv('PROXY_LOGIN')
proxy_password = os.getenv('PROXY_PASSWORD')
proxy_url = f"http://{proxy_login}:{proxy_password}@{proxy_host}:{proxy_port}"
os.environ['HTTP_PROXY'] = proxy_url
os.environ['HTTPS_PROXY'] = proxy_url

session = HTTP(
    testnet = False,
    api_key = os.getenv('BYBIT_API_KEY'),
    api_secret = os.getenv('BYBIT_SECRET')
)


# In[17]:


def get_balance(coin='USDT'):
    logger.info('Запрос баланса...')
    try:
        balance = session.get_wallet_balance(accountType='UNIFIED', coin=coin)
        return balance.get('result').get('list')[0].get('coin')[0].get('equity')
    except Exception as e:
        logger.error(f"Ошибка получения баланса: {e}")
        return None


# In[ ]:


def place_market_order(symbol, side, qty, tp, sl):
    order = None
    try:
        logger.info(f"📈 Отправка ордера: {side} {qty} {symbol}. TP={tp} SL={sl}")
        order = session.place_order(
            category=CATEGORY,
            symbol=symbol,
            side=side,
            qty=str(qty), 
            orderType='Market',
            marketUnit='baseCoin',
            takeProfit=str(tp),  
            stopLoss=str(sl)
)
        logger.info(f"✅ Ордер исполнен: {order}")      
        return order

    except Exception as e:
        logger.error(f"❌ Ошибка ордера: {e}")
        return None   

def open_long(symbol, qty, tp, sl):
    return place_market_order(symbol, 'Buy', qty, tp, sl)

def open_short(symbol, qty, tp, sl):
    return place_market_order(symbol, 'Sell', qty, tp, sl)

def close_position(symbol):
    btc_balance = get_balance(coin='BTC')
    if btc_balance and btc_balance > 0:
        closed_position = open_short('BTCUSDT', btc_balance)
        return closed_position
    else:
        logger.info("Нет позиции для закрытия")        
        return None


# In[ ]:


def test_connection():
    try:
        balance = get_balance('USDT')
        logger.info(f"✅ Подключение к Bybit успешно!")
        logger.info(f"💰 Баланс USDT: {balance}")    
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка подключения: {e}")        
        return False

