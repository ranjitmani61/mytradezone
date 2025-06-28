"""
Configuration settings for Professional Intraday Trading Assistant
"""

import os

# NSE Stocks (Top 100 most traded)
NSE_ALL_STOCKS = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'SBIN', 'ICICIBANK', 'BHARTIARTL', 'ITC',
    'KOTAKBANK', 'LT', 'HCLTECH', 'AXISBANK', 'ASIANPAINT', 'MARUTI', 'BAJFINANCE',
    'WIPRO', 'ULTRACEMCO', 'NESTLEIND', 'BAJAJFINSV', 'ONGC', 'TECHM', 'SUNPHARMA',
    'TATAMOTORS', 'POWERGRID', 'NTPC', 'COALINDIA', 'HDFCLIFE', 'SBILIFE', 'GRASIM',
    'ADANIPORTS', 'HINDALCO', 'JSWSTEEL', 'TATASTEEL', 'BPCL', 'DRREDDY', 'EICHERMOT',
    'CIPLA', 'INDUSINDBK', 'APOLLOHOSP', 'DIVISLAB', 'BAJAJ-AUTO', 'BRITANNIA',
    'SHREECEM', 'TITAN', 'VEDL', 'HEROMOTOCO', 'UPL', 'ADANIENT', 'PIDILITIND',
    'DMART', 'GODREJCP', 'M&M', 'ADANIGREEN', 'IOC', 'BANKBARODA', 'HINDUNILVR',
    'GAIL', 'DABUR', 'MARICO', 'LUPIN', 'BANDHANBNK', 'BERGEPAINT', 'NAUKRI',
    'SAIL', 'NMDC', 'JINDALSTEL', 'ZEEL', 'SIEMENS', 'AMBUJACEM', 'ACC', 'HAVELLS',
    'CONCOR', 'MCDOWELL-N', 'COLPAL', 'BIOCON', 'MOTHERSUMI', 'LICHSGFIN',
    'TORNTPHARM', 'PAGEIND', 'GODREJPROP', 'BOSCHLTD', 'AUROPHARMA', 'RAMCOCEM',
    'PEL', 'IDFCFIRSTB', 'CADILAHC', 'FEDERALBNK', 'JUBLFOOD', 'ASHOKLEY',
    'IBULHSGFIN', 'CUMMINSIND', 'BATAINDIA', 'PETRONET', 'MANAPPURAM', 'NATIONALUM',
    'SUNTV', 'VOLTAS', 'RBLBANK', 'MINDTREE', 'ESCORTS', 'DLF', 'CHOLAFIN'
]

# BSE Stocks
BSE_STOCKS = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'SBIN', 'ICICIBANK', 'BHARTIARTL',
    'ITC', 'KOTAKBANK', 'LT', 'HCLTECH', 'AXISBANK', 'ASIANPAINT', 'MARUTI'
]

# NIFTY 50 Stocks
NIFTY_50_STOCKS = [
    'ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV',
    'BPCL', 'BHARTIARTL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY',
    'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO',
    'HINDUNILVR', 'ICICIBANK', 'ITC', 'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK',
    'LT', 'M&M', 'MARUTI', 'NESTLEIND', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE',
    'SBILIFE', 'SBIN', 'SHREECEM', 'SUNPHARMA', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL',
    'TCS', 'TECHM', 'TITAN', 'UPL', 'ULTRACEMCO', 'WIPRO'
]

# Sector categorization
SECTORS = {
    'Banking': ['HDFCBANK', 'ICICIBANK', 'SBIN', 'KOTAKBANK', 'AXISBANK', 'INDUSINDBK'],
    'IT': ['TCS', 'INFY', 'HCLTECH', 'WIPRO', 'TECHM', 'MINDTREE'],
    'Auto': ['MARUTI', 'TATAMOTORS', 'BAJAJ-AUTO', 'HEROMOTOCO', 'M&M', 'EICHERMOT'],
    'Pharma': ['SUNPHARMA', 'DRREDDY', 'CIPLA', 'DIVISLAB', 'LUPIN', 'BIOCON'],
    'FMCG': ['HINDUNILVR', 'ITC', 'BRITANNIA', 'DABUR', 'MARICO', 'GODREJCP'],
    'Energy': ['RELIANCE', 'ONGC', 'BPCL', 'IOC', 'GAIL', 'COALINDIA'],
    'Telecom': ['BHARTIARTL', 'VODAIDEA'],
    'Metals': ['TATASTEEL', 'JSWSTEEL', 'HINDALCO', 'VEDL', 'SAIL', 'JINDALSTEL']
}

# Default watchlist for new users
DEFAULT_WATCHLIST = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'SBIN', 'ICICIBANK', 'BHARTIARTL',
    'ITC', 'KOTAKBANK', 'LT', 'HCLTECH', 'AXISBANK', 'ASIANPAINT', 'MARUTI',
    'BAJFINANCE', 'WIPRO', 'ULTRACEMCO', 'NESTLEIND', 'BAJAJFINSV', 'ONGC'
]

# Trading configuration
TRADING_CONFIG = {
    'timeframes': ['1m', '2m', '3m', '5m', '10m', '15m', '30m', '1h', '1d'],
    'default_timeframe': '5m',
    'default_period': '1d',
    'market_open_time': '09:15',
    'market_close_time': '15:30',
    'trading_days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'max_watchlist_size': 50,
    'min_price_filter': 10.0,
    'max_price_filter': 5000.0
}

# Chart configuration
CHART_CONFIG = {
    'height': 600,
    'width': None,
    'candlestick_colors': {
        'increasing': '#00ff00',
        'decreasing': '#ff0000'
    },
    'volume_colors': {
        'increasing': '#00ff00',
        'decreasing': '#ff0000'
    },
    'indicator_colors': {
        'sma': '#ff9500',
        'ema': '#0066cc',
        'rsi': '#9500ff',
        'macd': '#ff0095',
        'bb_upper': '#00ccff',
        'bb_lower': '#00ccff',
        'bb_middle': '#0066cc'
    }
}

# AI and ML configuration
AI_CONFIG = {
    'models': {
        'signal_generator': {
            'features': ['rsi', 'macd', 'bb_position', 'volume_ratio', 'price_change'],
            'lookback_periods': 20,
            'prediction_horizon': 1
        },
        'risk_assessment': {
            'features': ['volatility', 'atr', 'beta', 'correlation'],
            'risk_levels': ['Low', 'Medium', 'High']
        }
    },
    'thresholds': {
        'buy_confidence': 70,
        'sell_confidence': 70,
        'hold_range': [30, 70]
    }
}

# Telegram configuration
TELEGRAM_CONFIG = {
    'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN'),
    'chat_id': os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID'),
    'bot_username': '@MyStockSentryBot',
    'enable_alerts': True,
    'alert_types': {
        'trading_signals': True,
        'volume_alerts': True,
        'price_breakouts': True,
        'market_updates': True
    }
}

# Alert configuration
ALERT_CONFIG = {
    'volume_surge_threshold': 2.0,  # 2x average volume
    'price_change_threshold': 3.0,  # 3% price change
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'max_alerts_per_hour': 20,
    'cooldown_period': 300  # 5 minutes in seconds
}

# Technical indicator parameters
INDICATOR_CONFIG = {
    'rsi': {'period': 14},
    'macd': {'fast': 12, 'slow': 26, 'signal': 9},
    'bollinger_bands': {'period': 20, 'std_dev': 2},
    'sma': {'periods': [5, 10, 20, 50, 200]},
    'ema': {'periods': [5, 10, 12, 20, 26, 50]},
    'atr': {'period': 14},
    'stochastic': {'k_period': 14, 'd_period': 3},
    'williams_r': {'period': 14}
}

# Fibonacci retracement levels
FIBONACCI_LEVELS = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]

# Support and resistance configuration
SUPPORT_RESISTANCE_CONFIG = {
    'min_touches': 2,
    'tolerance': 0.02,  # 2% tolerance
    'lookback_periods': 50
}

# Market sessions (IST)
MARKET_SESSIONS = {
    'pre_market': {'start': '09:00', 'end': '09:15'},
    'regular': {'start': '09:15', 'end': '15:30'},
    'post_market': {'start': '15:30', 'end': '16:00'}
}

# Default features for ML models
DEFAULT_FEATURES = [
    'open', 'high', 'low', 'close', 'volume',
    'rsi', 'macd', 'macd_signal', 'macd_histogram',
    'bb_upper', 'bb_middle', 'bb_lower', 'bb_width',
    'sma_5', 'sma_10', 'sma_20', 'sma_50',
    'ema_12', 'ema_26', 'atr', 'volume_ratio'
]

# Risk management configuration
RISK_CONFIG = {
    'max_position_size': 0.1,  # 10% of portfolio
    'max_daily_loss': 0.02,    # 2% of portfolio
    'max_correlation': 0.7,     # Maximum correlation between positions
    'default_stop_loss': 0.02,  # 2% stop loss
    'default_take_profit': 0.04, # 4% take profit
    'risk_reward_ratio': 2.0    # Minimum risk-reward ratio
}

# Backtesting configuration
BACKTEST_CONFIG = {
    'initial_capital': 100000,
    'commission': 0.001,  # 0.1%
    'slippage': 0.0005,   # 0.05%
    'benchmark': 'NIFTY50',
    'rebalance_frequency': 'weekly',
    'max_positions': 10
}

# Performance metrics to track
PERFORMANCE_METRICS = [
    'total_return', 'annualized_return', 'volatility', 'sharpe_ratio',
    'max_drawdown', 'win_rate', 'profit_factor', 'avg_win', 'avg_loss',
    'total_trades', 'winning_trades', 'losing_trades'
]

# Data source configuration
DATA_CONFIG = {
    'primary_source': 'yfinance',
    'backup_sources': ['alpha_vantage', 'quandl'],
    'cache_duration': 300,  # 5 minutes
    'retry_attempts': 3,
    'timeout': 30
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'trading_assistant.log',
    'max_bytes': 10485760,  # 10MB
    'backup_count': 5
}