"""
Enhanced data fetching module with robust error handling
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import streamlit as st
import warnings
import time
warnings.filterwarnings('ignore')
from config import DATA_CONFIG
from utils import is_trading_time

class DataFetcher:
    def __init__(self):
        self.cache_duration = DATA_CONFIG['cache_duration']  # 5 minutes
        self.max_retries = DATA_CONFIG['retry_attempts']  # 3
        self.retry_delay = 1  # seconds
        
    @st.cache_data(ttl=300, show_spinner=False)
    def get_stock_data(_self, symbol: str, period: str = '1d', interval: str = '5m') -> pd.DataFrame:
        """Fetch stock data from yfinance with robust error handling and caching"""
        try:
            # Add .NS suffix for NSE stocks if not present
            if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
                symbol = f"{symbol}.NS"
            
            # Retry mechanism for better reliability
            for attempt in range(_self.max_retries):
                try:
                    # Create ticker object
                    ticker = yf.Ticker(symbol)
                    
                    # Fetch data with timeout
                    data = ticker.history(period=period, interval=interval, timeout=10)
                    
                    if data.empty:
                        if attempt < _self.max_retries - 1:
                            time.sleep(_self.retry_delay)
                            continue
                        else:
                            return pd.DataFrame()
                    
                    # Clean and validate data
                    data = data.dropna()
                    
                    # Ensure we have minimum required data
                    if len(data) < 2:
                        return pd.DataFrame()
                    
                    # Reset index to make datetime a column
                    data.reset_index(inplace=True)
                    
                    # Ensure numeric columns
                    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce')
                    
                    # Remove any remaining NaN rows
                    data = data.dropna()
                    
                    return data
                    
                except Exception as e:
                    if attempt < _self.max_retries - 1:
                        time.sleep(_self.retry_delay * (attempt + 1))
                        continue
                    else:
                        print(f"Error fetching data for {symbol} after {_self.max_retries} attempts: {str(e)}")
                        return pd.DataFrame()
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Critical error in get_stock_data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
    def get_stock_info(_self, symbol: str) -> Dict[str, Any]:
        """Get stock information with error handling"""
        try:
            if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
                symbol = f"{symbol}.NS"
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Return safe defaults if info is incomplete
            return {
                'longName': info.get('longName', symbol.replace('.NS', '')),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'marketCap': info.get('marketCap', 0),
                'previousClose': info.get('previousClose', 0),
                'regularMarketPrice': info.get('regularMarketPrice', 0),
                'volume': info.get('volume', 0),
                'averageVolume': info.get('averageVolume', 0),
                'beta': info.get('beta', 1.0),
                'trailingPE': info.get('trailingPE', 0),
                'dividendYield': info.get('dividendYield', 0)
            }
            
        except Exception as e:
            print(f"Error fetching info for {symbol}: {str(e)}")
            return {
                'longName': symbol.replace('.NS', ''),
                'sector': 'Unknown',
                'industry': 'Unknown',
                'marketCap': 0,
                'previousClose': 0,
                'regularMarketPrice': 0,
                'volume': 0,
                'averageVolume': 0,
                'beta': 1.0,
                'trailingPE': 0,
                'dividendYield': 0
            }
    
    def get_multiple_stocks_data(self, symbols: List[str], period: str = '1d', interval: str = '5m') -> Dict[str, pd.DataFrame]:
        """Fetch data for multiple stocks with progress tracking"""
        try:
            data_dict = {}
            
            # Use a simple progress tracking without Streamlit widgets
            successful_fetches = 0
            
            for i, symbol in enumerate(symbols):
                try:
                    data = self.get_stock_data(symbol, period, interval)
                    if not data.empty:
                        data_dict[symbol] = data
                        successful_fetches += 1
                    
                    # Small delay to avoid rate limiting
                    if i > 0 and i % 10 == 0:
                        time.sleep(0.1)
                        
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {str(e)}")
                    continue
            
            print(f"Successfully fetched data for {successful_fetches}/{len(symbols)} stocks")
            return data_dict
            
        except Exception as e:
            print(f"Error in get_multiple_stocks_data: {str(e)}")
            return {}
    
    def get_live_price(self, symbol: str) -> float:
        """Get current live price with fallback"""
        try:
            if not is_trading_time():
                return 0.0  # Return 0 when market is closed
            
            if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
                symbol = f"{symbol}.NS"
            
            ticker = yf.Ticker(symbol)
            
            # Try to get the most recent price
            data = ticker.history(period='1d', interval='1m')
            
            if not data.empty:
                return float(data['Close'].iloc[-1])
            else:
                # Fallback to longer period data
                data = ticker.history(period='1d', interval='5m')
                if not data.empty:
                    return float(data['Close'].iloc[-1])
                else:
                    return 0.0
                
        except Exception as e:
            print(f"Error getting live price for {symbol}: {str(e)}")
            return 0.0
    
    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get historical data for backtesting with better error handling"""
        try:
            if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
                symbol = f"{symbol}.NS"
            
            ticker = yf.Ticker(symbol)
            
            # Convert string dates to datetime if needed
            if isinstance(start_date, str):
                start_date = pd.to_datetime(start_date).date()
            if isinstance(end_date, str):
                end_date = pd.to_datetime(end_date).date()
            
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                print(f"No historical data available for {symbol}")
                return pd.DataFrame()
            
            # Clean and validate data
            data = data.dropna()
            
            # Ensure numeric columns
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_columns:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
            
            data = data.dropna()
            data.reset_index(inplace=True)
            
            return data
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def get_market_movers(self, limit: int = 20) -> Dict[str, List[Dict]]:
        """Get top gainers and losers with improved error handling"""
        try:
            from config import NIFTY_50_STOCKS
            
            gainers = []
            losers = []
            
            # Get data for all stocks first
            data_dict = self.get_multiple_stocks_data(NIFTY_50_STOCKS[:limit], period='1d', interval='5m')
            
            for symbol, data in data_dict.items():
                try:
                    if len(data) >= 2:
                        current_price = data['Close'].iloc[-1]
                        prev_price = data['Close'].iloc[-2]
                        change_pct = ((current_price - prev_price) / prev_price) * 100
                        
                        stock_data = {
                            'symbol': symbol,
                            'price': current_price,
                            'change_pct': change_pct,
                            'volume': data['Volume'].iloc[-1]
                        }
                        
                        if change_pct > 0:
                            gainers.append(stock_data)
                        else:
                            losers.append(stock_data)
                            
                except Exception as e:
                    print(f"Error processing market mover {symbol}: {str(e)}")
                    continue
            
            # Sort gainers and losers
            gainers.sort(key=lambda x: x['change_pct'], reverse=True)
            losers.sort(key=lambda x: x['change_pct'])
            
            return {
                'gainers': gainers[:10],
                'losers': losers[:10]
            }
            
        except Exception as e:
            print(f"Error getting market movers: {str(e)}")
            return {'gainers': [], 'losers': []}
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists and has data"""
        try:
            data = self.get_stock_data(symbol, period='1d', interval='5m')
            return not data.empty
            
        except Exception:
            return False