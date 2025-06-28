"""
AI-powered signal generation module with enhanced rule-based approach
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
import warnings
warnings.filterwarnings('ignore')
from config import AI_CONFIG
from technical_indicators import TechnicalIndicators

class AISignalGenerator:
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.config = AI_CONFIG
        
    def generate_signal(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Generate trading signal using enhanced rule-based approach"""
        try:
            tech_indicators = TechnicalIndicators()
            
            if data.empty or len(data) < 20:
                return self._get_default_signal(symbol)
            
            # Calculate technical indicators
            indicators = tech_indicators.calculate_all_indicators(data)
            
            if not indicators:
                return self._get_default_signal(symbol)
            
            # Enhanced rule-based signal generation
            signal_score = 0
            confidence_factors = []
            
            # RSI signals (weighted heavily)
            rsi = indicators.get('rsi', 50)
            if rsi < 25:  # Very oversold
                signal_score += 3
                confidence_factors.append(f"RSI very oversold ({rsi:.1f})")
            elif rsi < 30:  # Oversold
                signal_score += 2
                confidence_factors.append(f"RSI oversold ({rsi:.1f})")
            elif rsi > 75:  # Very overbought
                signal_score -= 3
                confidence_factors.append(f"RSI very overbought ({rsi:.1f})")
            elif rsi > 70:  # Overbought
                signal_score -= 2
                confidence_factors.append(f"RSI overbought ({rsi:.1f})")
            elif 45 <= rsi <= 55:  # Neutral zone
                signal_score += 0.5
            
            # MACD signals
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            macd_histogram = indicators.get('macd_histogram', 0)
            
            if macd > macd_signal and macd_histogram > 0:  # Bullish crossover
                signal_score += 1.5
                confidence_factors.append("MACD bullish crossover")
            elif macd < macd_signal and macd_histogram < 0:  # Bearish crossover
                signal_score -= 1.5
                confidence_factors.append("MACD bearish crossover")
            
            # Moving Average signals
            current_price = indicators.get('current_price', 0)
            sma_20 = indicators.get('sma_20', 0)
            sma_5 = indicators.get('sma_5', 0)
            ema_12 = indicators.get('ema_12', 0)
            
            if current_price > sma_20 and sma_20 > 0:  # Above SMA 20
                signal_score += 1
                confidence_factors.append("Price above SMA 20")
                
                if sma_5 > sma_20:  # Short MA above long MA
                    signal_score += 0.5
                    confidence_factors.append("Golden cross pattern")
                    
            elif current_price < sma_20 and sma_20 > 0:  # Below SMA 20
                signal_score -= 1
                confidence_factors.append("Price below SMA 20")
                
                if sma_5 < sma_20:  # Death cross pattern
                    signal_score -= 0.5
                    confidence_factors.append("Death cross pattern")
            
            # Bollinger Bands signals
            bb_upper = indicators.get('bb_upper', 0)
            bb_lower = indicators.get('bb_lower', 0)
            bb_middle = indicators.get('bb_middle', 0)
            
            if bb_upper > 0 and bb_lower > 0:
                if current_price <= bb_lower:  # At or below lower band
                    signal_score += 2
                    confidence_factors.append("Price at BB lower band")
                elif current_price >= bb_upper:  # At or above upper band
                    signal_score -= 2
                    confidence_factors.append("Price at BB upper band")
                elif current_price > bb_middle:  # Above middle band
                    signal_score += 0.5
            
            # Volume confirmation
            volume_ratio = indicators.get('volume_ratio', 1)
            if volume_ratio > 2:  # Very high volume
                signal_score *= 1.3
                confidence_factors.append(f"Very high volume ({volume_ratio:.1f}x)")
            elif volume_ratio > 1.5:  # High volume
                signal_score *= 1.2
                confidence_factors.append(f"High volume ({volume_ratio:.1f}x)")
            elif volume_ratio < 0.5:  # Very low volume
                signal_score *= 0.7
                confidence_factors.append("Low volume concern")
            
            # Price momentum
            price_change = indicators.get('price_change', 0)
            if abs(price_change) > 3:  # Strong momentum
                if price_change > 0:
                    signal_score += 1
                    confidence_factors.append(f"Strong upward momentum ({price_change:+.1f}%)")
                else:
                    signal_score -= 1
                    confidence_factors.append(f"Strong downward momentum ({price_change:+.1f}%)")
            elif abs(price_change) > 1.5:  # Moderate momentum
                if price_change > 0:
                    signal_score += 0.5
                else:
                    signal_score -= 0.5
            
            # ATR-based volatility check
            atr = indicators.get('atr', 0)
            if current_price > 0 and atr > 0:
                atr_pct = (atr / current_price) * 100
                if atr_pct > 5:  # High volatility
                    signal_score *= 0.9  # Reduce confidence slightly
                    confidence_factors.append("High volatility warning")
            
            # Support and resistance levels
            support = indicators.get('support', 0)
            resistance = indicators.get('resistance', 0)
            
            if support > 0 and current_price <= support * 1.02:  # Near support
                signal_score += 1
                confidence_factors.append("Near support level")
            elif resistance > 0 and current_price >= resistance * 0.98:  # Near resistance
                signal_score -= 1
                confidence_factors.append("Near resistance level")
            
            # Determine final signal based on enhanced scoring
            if signal_score >= 3:
                signal = 'BUY'
                confidence = min(90, 60 + abs(signal_score) * 8)
            elif signal_score <= -3:
                signal = 'SELL'
                confidence = min(90, 60 + abs(signal_score) * 8)
            elif signal_score >= 1.5:
                signal = 'BUY'
                confidence = min(75, 50 + abs(signal_score) * 10)
            elif signal_score <= -1.5:
                signal = 'SELL'
                confidence = min(75, 50 + abs(signal_score) * 10)
            else:
                signal = 'HOLD'
                confidence = 50 + abs(signal_score) * 5
            
            # Ensure confidence is within reasonable bounds
            confidence = max(30, min(95, confidence))
            
            return {
                'signal': signal,
                'confidence': round(confidence, 1),
                'price': current_price,
                'rsi': rsi,
                'macd': macd,
                'volume': indicators.get('current_volume', 0),
                'volume_ratio': volume_ratio,
                'signal_score': signal_score,
                'factors': confidence_factors[:5],  # Top 5 factors
                'timestamp': pd.Timestamp.now(),
                'symbol': symbol,
                'atr_percentage': (atr / current_price * 100) if current_price > 0 and atr > 0 else 0
            }
            
        except Exception as e:
            print(f"Error generating signal for {symbol}: {str(e)}")
            return self._get_default_signal(symbol)
    
    def _get_default_signal(self, symbol: str) -> Dict[str, Any]:
        """Return default signal when calculation fails"""
        return {
            'signal': 'HOLD',
            'confidence': 50.0,
            'price': 0.0,
            'rsi': 50.0,
            'macd': 0.0,
            'volume': 0,
            'volume_ratio': 1.0,
            'signal_score': 0,
            'factors': ['Insufficient data'],
            'timestamp': pd.Timestamp.now(),
            'symbol': symbol,
            'atr_percentage': 0
        }
    
    def batch_generate_signals(self, data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
        """Generate signals for multiple stocks"""
        try:
            signals = {}
            
            for symbol, data in data_dict.items():
                signals[symbol] = self.generate_signal(data, symbol)
            
            return signals
            
        except Exception as e:
            print(f"Error in batch signal generation: {str(e)}")
            return {}
    
    def get_signal_strength(self, signal_data: Dict[str, Any]) -> str:
        """Get signal strength description"""
        try:
            confidence = signal_data.get('confidence', 50)
            
            if confidence >= 85:
                return "Very Strong"
            elif confidence >= 75:
                return "Strong"
            elif confidence >= 65:
                return "Moderate"
            elif confidence >= 55:
                return "Weak"
            else:
                return "Very Weak"
                
        except Exception:
            return "Unknown"
    
    def validate_signal(self, signal_data: Dict[str, Any]) -> bool:
        """Validate if signal is reliable"""
        try:
            confidence = signal_data.get('confidence', 0)
            signal = signal_data.get('signal', 'HOLD')
            
            # Minimum confidence threshold
            if confidence < self.config['thresholds']['buy_confidence'] and signal != 'HOLD':
                return False
            
            # Check if key indicators are available
            required_fields = ['price', 'rsi', 'macd']
            for field in required_fields:
                if field not in signal_data:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def get_risk_assessment(self, data: pd.DataFrame, signal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk for the generated signal"""
        try:
            if data.empty:
                return {'risk_level': 'High', 'risk_score': 80, 'volatility': 0, 'atr_percentage': 0}
            
            # Calculate volatility
            if len(data) >= 20:
                returns = data['Close'].pct_change().dropna()
                volatility = returns.std() * np.sqrt(252) * 100 if len(returns) > 0 else 0  # Annualized volatility
            else:
                volatility = 0
            
            # ATR-based risk
            atr_pct = signal_data.get('atr_percentage', 0)
            
            # Risk score calculation
            risk_score = 0
            
            # Volatility component (0-35 points)
            if volatility > 50:
                risk_score += 35
            elif volatility > 35:
                risk_score += 25
            elif volatility > 20:
                risk_score += 15
            else:
                risk_score += 5
            
            # ATR component (0-25 points)
            if atr_pct > 6:
                risk_score += 25
            elif atr_pct > 4:
                risk_score += 18
            elif atr_pct > 2:
                risk_score += 10
            else:
                risk_score += 3
            
            # Signal confidence component (0-25 points)
            confidence = signal_data.get('confidence', 50)
            confidence_risk = (100 - confidence) * 0.25
            risk_score += confidence_risk
            
            # Volume component (0-15 points)
            volume_ratio = signal_data.get('volume_ratio', 1)
            if volume_ratio < 0.5:  # Very low volume
                risk_score += 15
            elif volume_ratio < 0.8:  # Low volume
                risk_score += 10
            elif volume_ratio > 3:  # Very high volume (can be risky)
                risk_score += 8
            elif volume_ratio > 2:  # High volume
                risk_score += 3
            
            # Market conditions component (0-10 points)
            rsi = signal_data.get('rsi', 50)
            if rsi > 80 or rsi < 20:  # Extreme RSI
                risk_score += 10
            elif rsi > 75 or rsi < 25:  # Very high/low RSI
                risk_score += 6
            
            # Determine risk level
            if risk_score >= 75:
                risk_level = 'High'
            elif risk_score >= 50:
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
            
            return {
                'risk_level': risk_level,
                'risk_score': min(100, max(0, round(risk_score))),
                'volatility': round(volatility, 2),
                'atr_percentage': round(atr_pct, 2)
            }
            
        except Exception as e:
            print(f"Error in risk assessment: {str(e)}")
            return {'risk_level': 'High', 'risk_score': 80, 'volatility': 0, 'atr_percentage': 0}
    
    def get_signal_quality_score(self, signal_data: Dict[str, Any]) -> int:
        """Calculate overall signal quality score (0-100)"""
        try:
            score = 0
            
            # Confidence component (40% weight)
            confidence = signal_data.get('confidence', 50)
            score += (confidence / 100) * 40
            
            # Factor count component (20% weight)
            factors = signal_data.get('factors', [])
            factor_score = min(len(factors) / 5, 1) * 20
            score += factor_score
            
            # Volume confirmation (20% weight)
            volume_ratio = signal_data.get('volume_ratio', 1)
            if volume_ratio >= 1.5:
                score += 20
            elif volume_ratio >= 1.2:
                score += 15
            elif volume_ratio >= 1:
                score += 10
            else:
                score += 5
            
            # Signal strength component (20% weight)
            signal_score = abs(signal_data.get('signal_score', 0))
            if signal_score >= 3:
                score += 20
            elif signal_score >= 2:
                score += 15
            elif signal_score >= 1:
                score += 10
            else:
                score += 5
            
            return min(100, max(0, round(score)))
            
        except Exception:
            return 50