"""
Stock scanner module for identifying trading opportunities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import streamlit as st
from config import ALERT_CONFIG

class StockScanner:
    def __init__(self):
        self.scan_results = []
        self.config = ALERT_CONFIG
        
    def scan_volume_surge(self, data_dict: Dict[str, pd.DataFrame], threshold: float = None) -> List[Dict[str, Any]]:
        """Scan for volume surge candidates"""
        threshold = threshold or self.config['volume_surge_threshold']
        try:
            volume_alerts = []
            
            for symbol, data in data_dict.items():
                try:
                    if data.empty or len(data) < 20:
                        continue
                    
                    # Calculate volume metrics
                    current_volume = data['Volume'].iloc[-1]
                    avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
                    
                    if avg_volume > 0:
                        volume_ratio = current_volume / avg_volume
                        
                        if volume_ratio >= threshold:
                            volume_alerts.append({
                                'symbol': symbol,
                                'volume_ratio': volume_ratio,
                                'current_volume': current_volume,
                                'avg_volume': avg_volume,
                                'price': data['Close'].iloc[-1],
                                'change_pct': ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100,
                                'scan_type': 'Volume Surge',
                                'timestamp': datetime.now()
                            })
                            
                except Exception as e:
                    print(f"Error scanning volume for {symbol}: {str(e)}")
                    continue
            
            # Sort by volume ratio
            volume_alerts.sort(key=lambda x: x['volume_ratio'], reverse=True)
            return volume_alerts[:20]  # Top 20
            
        except Exception as e:
            st.error(f"Volume surge scan error: {str(e)}")
            return []
    
    def scan_price_breakouts(self, data_dict: Dict[str, pd.DataFrame], period: int = 20) -> List[Dict[str, Any]]:
        """Scan for price breakout candidates"""
        try:
            breakout_alerts = []
            
            for symbol, data in data_dict.items():
                try:
                    if data.empty or len(data) < period + 5:
                        continue
                    
                    # Calculate resistance level (highest high in period)
                    resistance = data['High'].rolling(period).max().iloc[-2]  # Previous period
                    current_price = data['Close'].iloc[-1]
                    current_high = data['High'].iloc[-1]
                    
                    # Check for breakout
                    if current_high > resistance and current_price > resistance * 1.005:  # 0.5% buffer
                        price_change = ((current_price - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
                        
                        breakout_alerts.append({
                            'symbol': symbol,
                            'breakout_level': resistance,
                            'current_price': current_price,
                            'breakout_strength': (current_price - resistance) / resistance * 100,
                            'volume_ratio': data['Volume'].iloc[-1] / data['Volume'].rolling(20).mean().iloc[-1],
                            'change_pct': price_change,
                            'scan_type': 'Price Breakout',
                            'timestamp': datetime.now()
                        })
                        
                except Exception as e:
                    print(f"Error scanning breakouts for {symbol}: {str(e)}")
                    continue
            
            # Sort by breakout strength
            breakout_alerts.sort(key=lambda x: x['breakout_strength'], reverse=True)
            return breakout_alerts[:15]  # Top 15
            
        except Exception as e:
            st.error(f"Price breakout scan error: {str(e)}")
            return []
    
    def scan_price_breakdowns(self, data_dict: Dict[str, pd.DataFrame], period: int = 20) -> List[Dict[str, Any]]:
        """Scan for price breakdown candidates"""
        try:
            breakdown_alerts = []
            
            for symbol, data in data_dict.items():
                try:
                    if data.empty or len(data) < period + 5:
                        continue
                    
                    # Calculate support level (lowest low in period)
                    support = data['Low'].rolling(period).min().iloc[-2]  # Previous period
                    current_price = data['Close'].iloc[-1]
                    current_low = data['Low'].iloc[-1]
                    
                    # Check for breakdown
                    if current_low < support and current_price < support * 0.995:  # 0.5% buffer
                        price_change = ((current_price - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
                        
                        breakdown_alerts.append({
                            'symbol': symbol,
                            'breakdown_level': support,
                            'current_price': current_price,
                            'breakdown_strength': abs((current_price - support) / support * 100),
                            'volume_ratio': data['Volume'].iloc[-1] / data['Volume'].rolling(20).mean().iloc[-1],
                            'change_pct': price_change,
                            'scan_type': 'Price Breakdown',
                            'timestamp': datetime.now()
                        })
                        
                except Exception as e:
                    print(f"Error scanning breakdowns for {symbol}: {str(e)}")
                    continue
            
            # Sort by breakdown strength
            breakdown_alerts.sort(key=lambda x: x['breakdown_strength'], reverse=True)
            return breakdown_alerts[:15]  # Top 15
            
        except Exception as e:
            st.error(f"Price breakdown scan error: {str(e)}")
            return []
    
    def scan_gap_stocks(self, data_dict: Dict[str, pd.DataFrame], min_gap: float = None) -> List[Dict[str, Any]]:
        """Scan for gap up/down stocks"""
        min_gap = min_gap or self.config['price_change_threshold']
        try:
            gap_alerts = []
            
            for symbol, data in data_dict.items():
                try:
                    if data.empty or len(data) < 2:
                        continue
                    
                    # Calculate gap
                    prev_close = data['Close'].iloc[-2]
                    current_open = data['Open'].iloc[-1]
                    
                    gap_pct = ((current_open - prev_close) / prev_close) * 100
                    
                    if abs(gap_pct) >= min_gap:
                        gap_type = 'Gap Up' if gap_pct > 0 else 'Gap Down'
                        
                        gap_alerts.append({
                            'symbol': symbol,
                            'gap_percentage': gap_pct,
                            'prev_close': prev_close,
                            'current_open': current_open,
                            'current_price': data['Close'].iloc[-1],
                            'volume_ratio': data['Volume'].iloc[-1] / data['Volume'].rolling(20).mean().iloc[-1] if len(data) >= 20 else 1,
                            'scan_type': gap_type,
                            'timestamp': datetime.now()
                        })
                        
                except Exception as e:
                    print(f"Error scanning gaps for {symbol}: {str(e)}")
                    continue
            
            # Sort by gap percentage
            gap_alerts.sort(key=lambda x: abs(x['gap_percentage']), reverse=True)
            return gap_alerts[:15]  # Top 15
            
        except Exception as e:
            st.error(f"Gap scan error: {str(e)}")
            return []
    
    def scan_rsi_extremes(self, data_dict: Dict[str, pd.DataFrame], 
                         overbought: float = None, oversold: float = None) -> List[Dict[str, Any]]:
        """Scan for RSI extreme readings"""
        overbought = overbought or self.config['rsi_overbought']
        oversold = oversold or self.config['rsi_oversold']
        try:
            from technical_indicators import TechnicalIndicators
            tech_indicators = TechnicalIndicators()
            
            rsi_alerts = []
            
            for symbol, data in data_dict.items():
                try:
                    if data.empty or len(data) < 20:
                        continue
                    
                    # Calculate RSI
                    rsi = tech_indicators.calculate_rsi(data, 14)
                    
                    if len(rsi.dropna()) == 0:
                        continue
                    
                    current_rsi = rsi.iloc[-1]
                    
                    if current_rsi >= overbought or current_rsi <= oversold:
                        condition = 'Overbought' if current_rsi >= overbought else 'Oversold'
                        
                        rsi_alerts.append({
                            'symbol': symbol,
                            'rsi': current_rsi,
                            'condition': condition,
                            'price': data['Close'].iloc[-1],
                            'change_pct': ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100,
                            'volume_ratio': data['Volume'].iloc[-1] / data['Volume'].rolling(20).mean().iloc[-1] if len(data) >= 20 else 1,
                            'scan_type': f'RSI {condition}',
                            'timestamp': datetime.now()
                        })
                        
                except Exception as e:
                    print(f"Error scanning RSI for {symbol}: {str(e)}")
                    continue
            
            # Sort by RSI extreme
            rsi_alerts.sort(key=lambda x: abs(x['rsi'] - 50), reverse=True)
            return rsi_alerts[:20]  # Top 20
            
        except Exception as e:
            st.error(f"RSI scan error: {str(e)}")
            return []
    
    def scan_moving_average_crossovers(self, data_dict: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """Scan for moving average crossovers"""
        try:
            from technical_indicators import TechnicalIndicators
            tech_indicators = TechnicalIndicators()
            
            crossover_alerts = []
            
            for symbol, data in data_dict.items():
                try:
                    if data.empty or len(data) < 50:
                        continue
                    
                    # Calculate moving averages
                    sma_short = tech_indicators.calculate_sma(data, 20)
                    sma_long = tech_indicators.calculate_sma(data, 50)
                    
                    if len(sma_short.dropna()) < 2 or len(sma_long.dropna()) < 2:
                        continue
                    
                    # Check for crossover
                    current_short = sma_short.iloc[-1]
                    current_long = sma_long.iloc[-1]
                    prev_short = sma_short.iloc[-2]
                    prev_long = sma_long.iloc[-2]
                    
                    # Golden cross (bullish) or Death cross (bearish)
                    if prev_short <= prev_long and current_short > current_long:
                        crossover_type = 'Golden Cross'
                    elif prev_short >= prev_long and current_short < current_long:
                        crossover_type = 'Death Cross'
                    else:
                        continue
                    
                    crossover_alerts.append({
                        'symbol': symbol,
                        'crossover_type': crossover_type,
                        'sma_20': current_short,
                        'sma_50': current_long,
                        'price': data['Close'].iloc[-1],
                        'change_pct': ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100,
                        'volume_ratio': data['Volume'].iloc[-1] / data['Volume'].rolling(20).mean().iloc[-1] if len(data) >= 20 else 1,
                        'scan_type': f'MA {crossover_type}',
                        'timestamp': datetime.now()
                    })
                    
                except Exception as e:
                    print(f"Error scanning MA crossovers for {symbol}: {str(e)}")
                    continue
            
            return crossover_alerts
            
        except Exception as e:
            st.error(f"MA crossover scan error: {str(e)}")
            return []
    
    def comprehensive_scan(self, stock_list: List[str], data_fetcher) -> Dict[str, List[Dict[str, Any]]]:
        """Perform comprehensive scan with all strategies"""
        try:
            # Fetch data for all stocks
            with st.spinner("Fetching market data..."):
                data_dict = data_fetcher.get_multiple_stocks_data(stock_list, period='1d', interval='5m')
            
            if not data_dict:
                st.error("No data available for scanning")
                return {}
            
            st.info(f"Scanning {len(data_dict)} stocks...")
            
            scan_results = {}
            
            # Volume surge scan
            with st.spinner("Scanning for volume surges..."):
                scan_results['volume_surge'] = self.scan_volume_surge(data_dict)
            
            # Price breakout scan
            with st.spinner("Scanning for price breakouts..."):
                scan_results['breakouts'] = self.scan_price_breakouts(data_dict)
            
            # Price breakdown scan
            with st.spinner("Scanning for price breakdowns..."):
                scan_results['breakdowns'] = self.scan_price_breakdowns(data_dict)
            
            # Gap scan
            with st.spinner("Scanning for gap moves..."):
                scan_results['gaps'] = self.scan_gap_stocks(data_dict)
            
            # RSI extremes scan
            with st.spinner("Scanning for RSI extremes..."):
                scan_results['rsi_extremes'] = self.scan_rsi_extremes(data_dict)
            
            # Moving average crossovers
            with st.spinner("Scanning for MA crossovers..."):
                scan_results['ma_crossovers'] = self.scan_moving_average_crossovers(data_dict)
            
            return scan_results
            
        except Exception as e:
            st.error(f"Comprehensive scan error: {str(e)}")
            return {}
    
    def get_scan_summary(self, scan_results: Dict[str, List[Dict[str, Any]]]) -> Dict[str, int]:
        """Get summary of scan results"""
        try:
            summary = {}
            
            for scan_type, results in scan_results.items():
                summary[scan_type] = len(results)
            
            summary['total_opportunities'] = sum(summary.values())
            
            return summary
            
        except Exception as e:
            print(f"Error creating scan summary: {str(e)}")
            return {}
    
    def filter_scan_results(self, scan_results: Dict[str, List[Dict[str, Any]]], 
                           filters: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Filter scan results based on criteria"""
        try:
            filtered_results = {}
            
            for scan_type, results in scan_results.items():
                filtered_list = []
                
                for result in results:
                    # Apply filters
                    if 'min_price' in filters:
                        if result.get('current_price', result.get('price', 0)) < filters['min_price']:
                            continue
                    
                    if 'max_price' in filters:
                        if result.get('current_price', result.get('price', 0)) > filters['max_price']:
                            continue
                    
                    if 'min_volume_ratio' in filters:
                        if result.get('volume_ratio', 1) < filters['min_volume_ratio']:
                            continue
                    
                    if 'symbols' in filters and filters['symbols']:
                        if result.get('symbol') not in filters['symbols']:
                            continue
                    
                    filtered_list.append(result)
                
                filtered_results[scan_type] = filtered_list
            
            return filtered_results
            
        except Exception as e:
            print(f"Error filtering scan results: {str(e)}")
            return scan_results