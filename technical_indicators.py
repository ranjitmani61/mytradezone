"""
Technical indicators calculation module with fallback implementations
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from config import INDICATOR_CONFIG

class TechnicalIndicators:
    def __init__(self):
        self.config = INDICATOR_CONFIG
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = None) -> pd.Series:
        """Calculate RSI (Relative Strength Index) with fallback"""
        period = period or self.config['rsi']['period']
        try:
            # Try using TA-Lib if available
            try:
                import talib as ta
                return pd.Series(ta.RSI(data['Close'].values, timeperiod=period), index=data.index)
            except ImportError:
                pass
            
            # Fallback calculation
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
            
        except Exception as e:
            print(f"Error calculating RSI: {str(e)}")
            return pd.Series(index=data.index, dtype=float)
    
    def calculate_macd(self, data: pd.DataFrame, 
                      fast: int = None, slow: int = None, signal: int = None) -> Dict[str, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        macd_config = self.config['macd']
        fast = fast or macd_config['fast']
        slow = slow or macd_config['slow']
        signal = signal or macd_config['signal']
        
        try:
            # Try using TA-Lib if available
            try:
                import talib as ta
                macd, macd_signal, macd_histogram = ta.MACD(
                    data['Close'].values, 
                    fastperiod=fast, 
                    slowperiod=slow, 
                    signalperiod=signal
                )
                return {
                    'macd': pd.Series(macd, index=data.index),
                    'macd_signal': pd.Series(macd_signal, index=data.index),
                    'macd_histogram': pd.Series(macd_histogram, index=data.index)
                }
            except ImportError:
                pass
            
            # Fallback calculation
            ema_fast = data['Close'].ewm(span=fast).mean()
            ema_slow = data['Close'].ewm(span=slow).mean()
            macd = ema_fast - ema_slow
            macd_signal = macd.ewm(span=signal).mean()
            macd_histogram = macd - macd_signal
            
            return {
                'macd': macd,
                'macd_signal': macd_signal,
                'macd_histogram': macd_histogram
            }
            
        except Exception as e:
            print(f"Error calculating MACD: {str(e)}")
            return {
                'macd': pd.Series(index=data.index, dtype=float),
                'macd_signal': pd.Series(index=data.index, dtype=float),
                'macd_histogram': pd.Series(index=data.index, dtype=float)
            }
    
    def calculate_bollinger_bands(self, data: pd.DataFrame, 
                                 period: int = None, std_dev: int = None) -> Dict[str, pd.Series]:
        """Calculate Bollinger Bands"""
        bb_config = self.config['bollinger_bands']
        period = period or bb_config['period']
        std_dev = std_dev or bb_config['std_dev']
        
        try:
            # Try using TA-Lib if available
            try:
                import talib as ta
                bb_upper, bb_middle, bb_lower = ta.BBANDS(
                    data['Close'].values, 
                    timeperiod=period, 
                    nbdevup=std_dev, 
                    nbdevdn=std_dev
                )
                return {
                    'bb_upper': pd.Series(bb_upper, index=data.index),
                    'bb_middle': pd.Series(bb_middle, index=data.index),
                    'bb_lower': pd.Series(bb_lower, index=data.index)
                }
            except ImportError:
                pass
            
            # Fallback calculation
            sma = data['Close'].rolling(window=period).mean()
            std = data['Close'].rolling(window=period).std()
            
            return {
                'bb_upper': sma + (std * std_dev),
                'bb_middle': sma,
                'bb_lower': sma - (std * std_dev)
            }
            
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {str(e)}")
            return {
                'bb_upper': pd.Series(index=data.index, dtype=float),
                'bb_middle': pd.Series(index=data.index, dtype=float),
                'bb_lower': pd.Series(index=data.index, dtype=float)
            }
    
    def calculate_sma(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        try:
            # Try using TA-Lib if available
            try:
                import talib as ta
                return pd.Series(ta.SMA(data['Close'].values, timeperiod=period), index=data.index)
            except ImportError:
                pass
            
            # Fallback calculation
            return data['Close'].rolling(window=period).mean()
            
        except Exception as e:
            print(f"Error calculating SMA: {str(e)}")
            return pd.Series(index=data.index, dtype=float)
    
    def calculate_ema(self, data: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Exponential Moving Average"""
        try:
            # Try using TA-Lib if available
            try:
                import talib as ta
                return pd.Series(ta.EMA(data['Close'].values, timeperiod=period), index=data.index)
            except ImportError:
                pass
            
            # Fallback calculation
            return data['Close'].ewm(span=period).mean()
            
        except Exception as e:
            print(f"Error calculating EMA: {str(e)}")
            return pd.Series(index=data.index, dtype=float)
    
    def calculate_atr(self, data: pd.DataFrame, period: int = None) -> pd.Series:
        """Calculate Average True Range"""
        period = period or self.config['atr']['period']
        try:
            # Try using TA-Lib if available
            try:
                import talib as ta
                return pd.Series(ta.ATR(
                    data['High'].values, 
                    data['Low'].values, 
                    data['Close'].values, 
                    timeperiod=period
                ), index=data.index)
            except ImportError:
                pass
            
            # Fallback calculation
            high_low = data['High'] - data['Low']
            high_close = np.abs(data['High'] - data['Close'].shift())
            low_close = np.abs(data['Low'] - data['Close'].shift())
            
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = ranges.max(axis=1)
            
            return true_range.rolling(period).mean()
            
        except Exception as e:
            print(f"Error calculating ATR: {str(e)}")
            return pd.Series(index=data.index, dtype=float)
    
    def calculate_stochastic(self, data: pd.DataFrame, 
                            k_period: int = None, d_period: int = None) -> Dict[str, pd.Series]:
        """Calculate Stochastic Oscillator"""
        stoch_config = self.config['stochastic']
        k_period = k_period or stoch_config['k_period']
        d_period = d_period or stoch_config['d_period']
        
        try:
            # Try using TA-Lib if available
            try:
                import talib as ta
                slowk, slowd = ta.STOCH(
                    data['High'].values, 
                    data['Low'].values, 
                    data['Close'].values, 
                    fastk_period=k_period, 
                    slowk_period=d_period, 
                    slowd_period=d_period
                )
                return {
                    'stoch_k': pd.Series(slowk, index=data.index),
                    'stoch_d': pd.Series(slowd, index=data.index)
                }
            except ImportError:
                pass
            
            # Fallback calculation
            lowest_low = data['Low'].rolling(window=k_period).min()
            highest_high = data['High'].rolling(window=k_period).max()
            
            k_percent = 100 * ((data['Close'] - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=d_period).mean()
            
            return {
                'stoch_k': k_percent,
                'stoch_d': d_percent
            }
            
        except Exception as e:
            print(f"Error calculating Stochastic: {str(e)}")
            return {
                'stoch_k': pd.Series(index=data.index, dtype=float),
                'stoch_d': pd.Series(index=data.index, dtype=float)
            }
    
    def calculate_volume_sma(self, data: pd.DataFrame, period: int = 20) -> pd.Series:
        """Calculate Volume Simple Moving Average"""
        try:
            return data['Volume'].rolling(window=period).mean()
        except Exception as e:
            print(f"Error calculating Volume SMA: {str(e)}")
            return pd.Series(index=data.index, dtype=float)
    
    def calculate_volume_ratio(self, data: pd.DataFrame, period: int = 20) -> pd.Series:
        """Calculate Volume Ratio (current volume / average volume)"""
        try:
            volume_sma = self.calculate_volume_sma(data, period)
            return data['Volume'] / volume_sma
        except Exception as e:
            print(f"Error calculating Volume Ratio: {str(e)}")
            return pd.Series(index=data.index, dtype=float)
    
    def calculate_price_change(self, data: pd.DataFrame, periods: int = 1) -> pd.Series:
        """Calculate price change percentage"""
        try:
            return data['Close'].pct_change(periods) * 100
        except Exception as e:
            print(f"Error calculating Price Change: {str(e)}")
            return pd.Series(index=data.index, dtype=float)
    
    def calculate_support_resistance(self, data: pd.DataFrame, window: int = 20) -> Dict[str, float]:
        """Calculate basic support and resistance levels"""
        try:
            if len(data) < window:
                return {'support': 0, 'resistance': 0}
            
            # Use recent data for S&R calculation
            recent_data = data.tail(window)
            
            # Simple S&R based on min/max
            support = recent_data['Low'].min()
            resistance = recent_data['High'].max()
            
            return {
                'support': float(support),
                'resistance': float(resistance)
            }
            
        except Exception as e:
            print(f"Error calculating Support/Resistance: {str(e)}")
            return {'support': 0, 'resistance': 0}
    
    def calculate_pivot_points(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate Pivot Points"""
        try:
            if len(data) < 2:
                return {}
            
            # Use previous day's data
            high = data['High'].iloc[-2]
            low = data['Low'].iloc[-2]
            close = data['Close'].iloc[-2]
            
            pivot = (high + low + close) / 3
            
            r1 = 2 * pivot - low
            r2 = pivot + (high - low)
            r3 = high + 2 * (pivot - low)
            
            s1 = 2 * pivot - high
            s2 = pivot - (high - low)
            s3 = low - 2 * (high - pivot)
            
            return {
                'pivot': float(pivot),
                'r1': float(r1),
                'r2': float(r2),
                'r3': float(r3),
                's1': float(s1),
                's2': float(s2),
                's3': float(s3)
            }
            
        except Exception as e:
            print(f"Error calculating Pivot Points: {str(e)}")
            return {}
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate all technical indicators safely"""
        try:
            if data.empty or len(data) < 20:
                return {}
            
            indicators = {}
            
            # Basic indicators with safe fallbacks
            try:
                rsi_series = self.calculate_rsi(data)
                indicators['rsi'] = float(rsi_series.iloc[-1]) if not rsi_series.empty and len(rsi_series.dropna()) > 0 else 50.0
            except Exception:
                indicators['rsi'] = 50.0
            
            # MACD
            try:
                macd_data = self.calculate_macd(data)
                indicators['macd'] = float(macd_data['macd'].iloc[-1]) if not macd_data['macd'].empty and len(macd_data['macd'].dropna()) > 0 else 0.0
                indicators['macd_signal'] = float(macd_data['macd_signal'].iloc[-1]) if not macd_data['macd_signal'].empty and len(macd_data['macd_signal'].dropna()) > 0 else 0.0
                indicators['macd_histogram'] = float(macd_data['macd_histogram'].iloc[-1]) if not macd_data['macd_histogram'].empty and len(macd_data['macd_histogram'].dropna()) > 0 else 0.0
            except Exception:
                indicators['macd'] = 0.0
                indicators['macd_signal'] = 0.0
                indicators['macd_histogram'] = 0.0
            
            # Bollinger Bands
            try:
                bb_data = self.calculate_bollinger_bands(data)
                indicators['bb_upper'] = float(bb_data['bb_upper'].iloc[-1]) if not bb_data['bb_upper'].empty and len(bb_data['bb_upper'].dropna()) > 0 else 0.0
                indicators['bb_middle'] = float(bb_data['bb_middle'].iloc[-1]) if not bb_data['bb_middle'].empty and len(bb_data['bb_middle'].dropna()) > 0 else 0.0
                indicators['bb_lower'] = float(bb_data['bb_lower'].iloc[-1]) if not bb_data['bb_lower'].empty and len(bb_data['bb_lower'].dropna()) > 0 else 0.0
            except Exception:
                indicators['bb_upper'] = 0.0
                indicators['bb_middle'] = 0.0
                indicators['bb_lower'] = 0.0
            
            # Moving Averages
            try:
                sma_5_series = self.calculate_sma(data, 5)
                indicators['sma_5'] = float(sma_5_series.iloc[-1]) if not sma_5_series.empty and len(sma_5_series.dropna()) > 0 else 0.0
                
                sma_10_series = self.calculate_sma(data, 10)
                indicators['sma_10'] = float(sma_10_series.iloc[-1]) if not sma_10_series.empty and len(sma_10_series.dropna()) > 0 else 0.0
                
                sma_20_series = self.calculate_sma(data, 20)
                indicators['sma_20'] = float(sma_20_series.iloc[-1]) if not sma_20_series.empty and len(sma_20_series.dropna()) > 0 else 0.0
                
                ema_12_series = self.calculate_ema(data, 12)
                indicators['ema_12'] = float(ema_12_series.iloc[-1]) if not ema_12_series.empty and len(ema_12_series.dropna()) > 0 else 0.0
                
                ema_26_series = self.calculate_ema(data, 26)
                indicators['ema_26'] = float(ema_26_series.iloc[-1]) if not ema_26_series.empty and len(ema_26_series.dropna()) > 0 else 0.0
            except Exception:
                indicators['sma_5'] = 0.0
                indicators['sma_10'] = 0.0
                indicators['sma_20'] = 0.0
                indicators['ema_12'] = 0.0
                indicators['ema_26'] = 0.0
            
            # Other indicators
            try:
                atr_series = self.calculate_atr(data)
                indicators['atr'] = float(atr_series.iloc[-1]) if not atr_series.empty and len(atr_series.dropna()) > 0 else 0.0
                
                volume_ratio_series = self.calculate_volume_ratio(data)
                indicators['volume_ratio'] = float(volume_ratio_series.iloc[-1]) if not volume_ratio_series.empty and len(volume_ratio_series.dropna()) > 0 else 1.0
                
                price_change_series = self.calculate_price_change(data)
                indicators['price_change'] = float(price_change_series.iloc[-1]) if not price_change_series.empty and len(price_change_series.dropna()) > 0 else 0.0
            except Exception:
                indicators['atr'] = 0.0
                indicators['volume_ratio'] = 1.0
                indicators['price_change'] = 0.0
            
            # Support and Resistance
            try:
                sr_levels = self.calculate_support_resistance(data)
                indicators.update(sr_levels)
            except Exception:
                indicators['support'] = 0.0
                indicators['resistance'] = 0.0
            
            # Current price data
            try:
                indicators['current_price'] = float(data['Close'].iloc[-1])
                indicators['current_volume'] = float(data['Volume'].iloc[-1])
            except Exception:
                indicators['current_price'] = 0.0
                indicators['current_volume'] = 0.0
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating indicators: {str(e)}")
            return {
                'rsi': 50.0,
                'macd': 0.0,
                'macd_signal': 0.0,
                'macd_histogram': 0.0,
                'bb_upper': 0.0,
                'bb_middle': 0.0,
                'bb_lower': 0.0,
                'sma_5': 0.0,
                'sma_10': 0.0,
                'sma_20': 0.0,
                'ema_12': 0.0,
                'ema_26': 0.0,
                'atr': 0.0,
                'volume_ratio': 1.0,
                'price_change': 0.0,
                'support': 0.0,
                'resistance': 0.0,
                'current_price': 0.0,
                'current_volume': 0.0
            }