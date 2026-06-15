# strategy.py
# Торговая стратегия

def generating_signals(df, params):
        
    # Выгрузим данные в OHLC
    open_price = df['open']
    high = df['high']
    low = df['low']
    close = df['close']

    # Выгрузим параметры
    lookback = params['lookback']
    range_days = params['range_days']
    volatility = params['volatility']
    reward_risk = params['reward_risk']
    
    min_risk = 0.003
    n = len(close)
    current_date = len(open_price) - 1

    # Определение диапазона
    range_start = current_date - range_days - 1
    range_high = high.iloc[range_start:current_date-1].max().item()
    range_low = low.iloc[range_start:current_date-1].min().item()
    range_width = (range_high - range_low)/range_low

    is_narrow_range = range_width <= volatility

    if is_narrow_range:     
        if close.iloc[current_date-1].item() > range_high:
            entry_flag = 1
            stop_loss = open_price.iloc[current_date-1]
            risk = open_price.iloc[current_date].item() - stop_loss
            take_profit = open_price.iloc[current_date] + risk*reward_risk
            if risk<min_risk:
                entry_flag = 0
                stop_loss = None
                take_profit = None
            return entry_flag, take_profit, stop_loss
        elif close.iloc[current_date-1].item() < range_low:
            entry_flag = -1
            stop_loss = open_price.iloc[current_date-1]
            risk = stop_loss - open_price.iloc[current_date].item()
            take_profit = open_price.iloc[current_date] - risk*reward_risk
            if risk<min_risk:
                entry_flag = 0
                stop_loss = None
                take_profit = None
            return entry_flag, take_profit, stop_loss
    return 0, None, None

    
