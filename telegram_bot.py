"""
Telegram bot integration for trading alerts and commands
"""

import requests
import json
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional
import os

class TelegramBot:
    def __init__(self):
        # Get bot token from environment or config
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '7248457164:AAF-IAycn_9fGcJtm4IifjA68QaDPnvwivg')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID', '6253409461')
        self.bot_username = "@MyStockSentryBot"
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Initialize session state
        if 'telegram_connected' not in st.session_state:
            st.session_state.telegram_connected = False
        
        if 'telegram_messages' not in st.session_state:
            st.session_state.telegram_messages = []
    
    def send_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        """Send message to Telegram chat"""
        try:
            url = f"{self.base_url}/sendMessage"
            
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    return True
                else:
                    print(f"Telegram API error: {result.get('description', 'Unknown error')}")
                    return False
            else:
                print(f"HTTP error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error sending Telegram message: {str(e)}")
            return False
    
    def send_signal_alert(self, symbol: str, signal_data: Dict[str, Any]) -> bool:
        """Send trading signal alert via Telegram"""
        try:
            signal = signal_data.get('signal', 'HOLD')
            price = signal_data.get('price', 0)
            confidence = signal_data.get('confidence', 50)
            rsi = signal_data.get('rsi', 50)
            macd = signal_data.get('macd', 0)
            
            # Format message based on signal type
            if signal == 'BUY':
                emoji = '🟢'
                action = 'BUY SIGNAL'
                message = f"*{emoji} {action} DETECTED*\n\n"
            elif signal == 'SELL':
                emoji = '🔴'
                action = 'SELL SIGNAL'
                message = f"*{emoji} {action} DETECTED*\n\n"
            else:
                emoji = '🔵'
                action = 'HOLD SIGNAL'
                message = f"*{emoji} {action}*\n\n"
            
            message += f"📈 *Stock:* {symbol}\n"
            message += f"💰 *Price:* ₹{price:.2f}\n"
            message += f"🎯 *Confidence:* {confidence}%\n"
            message += f"📊 *RSI:* {rsi:.1f}\n"
            message += f"📈 *MACD:* {macd:.3f}\n"
            message += f"⏰ *Time:* {datetime.now().strftime('%d %b %Y, %H:%M:%S')}\n\n"
            message += f"🤖 *Professional Intraday Trading Assistant*\n"
            message += f"📱 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending signal alert: {str(e)}")
            return False
    
    def send_market_summary(self, gainers: List[Dict], losers: List[Dict]) -> bool:
        """Send market summary"""
        try:
            message = "*📊 MARKET SUMMARY*\n\n"
            
            # Top Gainers
            message += "*🟢 TOP GAINERS:*\n"
            for i, gainer in enumerate(gainers[:5], 1):
                symbol = gainer.get('symbol', '').replace('.NS', '')
                change = gainer.get('change_pct', 0)
                price = gainer.get('price', 0)
                message += f"{i}. {symbol}: ₹{price:.2f} (+{change:.1f}%)\n"
            
            message += "\n*🔴 TOP LOSERS:*\n"
            for i, loser in enumerate(losers[:5], 1):
                symbol = loser.get('symbol', '').replace('.NS', '')
                change = loser.get('change_pct', 0)
                price = loser.get('price', 0)
                message += f"{i}. {symbol}: ₹{price:.2f} ({change:.1f}%)\n"
            
            message += f"\n⏰ *Updated:* {datetime.now().strftime('%H:%M:%S')}"
            message += f"\n🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending market summary: {str(e)}")
            return False
    
    def send_watchlist_status(self, watchlist: List[str]) -> bool:
        """Send current watchlist status"""
        try:
            message = "*📋 CURRENT WATCHLIST*\n\n"
            
            for i, stock in enumerate(watchlist[:20], 1):  # Limit to 20 stocks
                message += f"{i}. {stock}\n"
            
            if len(watchlist) > 20:
                message += f"\n... and {len(watchlist) - 20} more stocks"
            
            message += f"\n📊 *Total Stocks:* {len(watchlist)}"
            message += f"\n⏰ *Updated:* {datetime.now().strftime('%H:%M:%S')}"
            message += f"\n🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending watchlist status: {str(e)}")
            return False
    
    def send_test_message(self) -> bool:
        """Send test message to verify connection"""
        try:
            message = "*🧪 TEST MESSAGE*\n\n"
            message += "✅ Telegram bot is working correctly!\n\n"
            message += "🤖 *Professional Intraday Trading Assistant*\n"
            message += f"📱 *Bot:* {self.bot_username}\n"
            message += f"👤 *Chat ID:* {self.chat_id}\n"
            message += f"⏰ *Time:* {datetime.now().strftime('%d %b %Y, %H:%M:%S')}\n\n"
            message += "Ready to receive trading alerts! 🚀"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending test message: {str(e)}")
            return False
    
    def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """Get bot information"""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    return result.get('result')
            
            return None
            
        except Exception as e:
            print(f"Error getting bot info: {str(e)}")
            return None
    
    def get_chat_info(self) -> Optional[Dict[str, Any]]:
        """Get chat information"""
        try:
            url = f"{self.base_url}/getChat"
            params = {'chat_id': self.chat_id}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    return result.get('result')
            
            return None
            
        except Exception as e:
            print(f"Error getting chat info: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """Test bot connection and update session state"""
        try:
            bot_info = self.get_bot_info()
            
            if bot_info:
                st.session_state.telegram_connected = True
                st.session_state.bot_username = bot_info.get('username', self.bot_username)
                return True
            else:
                st.session_state.telegram_connected = False
                return False
                
        except Exception as e:
            print(f"Error testing connection: {str(e)}")
            st.session_state.telegram_connected = False
            return False
    
    def send_volume_alert(self, symbol: str, volume_data: Dict[str, Any]) -> bool:
        """Send volume surge alert"""
        try:
            volume_ratio = volume_data.get('volume_ratio', 1.0)
            price = volume_data.get('price', 0)
            current_volume = volume_data.get('current_volume', 0)
            
            message = "*📊 VOLUME SURGE ALERT*\n\n"
            message += f"📈 *Stock:* {symbol}\n"
            message += f"💰 *Price:* ₹{price:.2f}\n"
            message += f"📊 *Volume:* {volume_ratio:.1f}x average\n"
            message += f"📈 *Current Volume:* {current_volume:,}\n"
            message += f"⏰ *Time:* {datetime.now().strftime('%H:%M:%S')}\n\n"
            message += f"⚡ *High volume activity detected!*\n"
            message += f"🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending volume alert: {str(e)}")
            return False
    
    def send_price_alert(self, symbol: str, price_data: Dict[str, Any]) -> bool:
        """Send price breakout/breakdown alert"""
        try:
            alert_type = price_data.get('alert_type', 'BREAKOUT')
            current_price = price_data.get('current_price', 0)
            target_price = price_data.get('target_price', 0)
            change_pct = price_data.get('change_pct', 0)
            
            emoji = '🚀' if alert_type == 'BREAKOUT' else '📉'
            
            message = f"*{emoji} {alert_type.upper()} ALERT*\n\n"
            message += f"📈 *Stock:* {symbol}\n"
            message += f"💰 *Current Price:* ₹{current_price:.2f}\n"
            message += f"🎯 *Target Price:* ₹{target_price:.2f}\n"
            message += f"📊 *Change:* {change_pct:+.1f}%\n"
            message += f"⏰ *Time:* {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            if alert_type == 'BREAKOUT':
                message += "🔥 *Price broke above resistance!*\n"
            else:
                message += "⚠️ *Price broke below support!*\n"
            
            message += f"🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending price alert: {str(e)}")
            return False
    
    def send_market_status(self) -> bool:
        """Send market status update"""
        try:
            current_time = datetime.now()
            is_market_hours = (9 <= current_time.hour <= 15) and (current_time.weekday() < 5)
            
            status_emoji = "🟢" if is_market_hours else "🔴"
            status_text = "OPEN" if is_market_hours else "CLOSED"
            
            message = f"*📊 MARKET STATUS UPDATE*\n\n"
            message += f"{status_emoji} *Market:* {status_text}\n"
            message += f"📅 *Date:* {current_time.strftime('%d %b %Y')}\n"
            message += f"⏰ *Time:* {current_time.strftime('%H:%M:%S')}\n\n"
            
            if is_market_hours:
                message += "✅ *Trading is active*\n"
                message += "📡 *Scanner is monitoring markets*\n"
            else:
                next_open = "9:15 AM" if current_time.hour < 9 else "9:15 AM (Next Day)"
                message += f"⏰ *Next Opening:* {next_open}\n"
                message += "💤 *Scanner in standby mode*\n"
            
            message += f"\n🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending market status: {str(e)}")
            return False
    
    def handle_bot_commands(self, command: str, data: Dict[str, Any] = None) -> bool:
        """Handle bot commands like /buylist, /selllist etc."""
        try:
            if command == '/buylist':
                return self._send_buy_list(data)
            elif command == '/selllist':
                return self._send_sell_list(data)
            elif command == '/status':
                return self.send_market_status()
            elif command == '/watchlist':
                watchlist = data.get('watchlist', []) if data else []
                return self.send_watchlist_status(watchlist)
            elif command == '/test':
                return self.send_test_message()
            else:
                return self._send_help_message()
                
        except Exception as e:
            print(f"Error handling bot command: {str(e)}")
            return False
    
    def _send_buy_list(self, data: Dict[str, Any]) -> bool:
        """Send list of buy signals"""
        try:
            buy_signals = data.get('buy_signals', []) if data else []
            
            message = "*🟢 BUY SIGNALS*\n\n"
            
            if buy_signals:
                for i, signal in enumerate(buy_signals[:10], 1):
                    symbol = signal.get('symbol', '')
                    price = signal.get('price', 0)
                    confidence = signal.get('confidence', 0)
                    message += f"{i}. *{symbol}* - ₹{price:.2f} ({confidence:.0f}%)\n"
            else:
                message += "No buy signals available at the moment.\n"
            
            message += f"\n⏰ *Updated:* {datetime.now().strftime('%H:%M:%S')}"
            message += f"\n🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending buy list: {str(e)}")
            return False
    
    def _send_sell_list(self, data: Dict[str, Any]) -> bool:
        """Send list of sell signals"""
        try:
            sell_signals = data.get('sell_signals', []) if data else []
            
            message = "*🔴 SELL SIGNALS*\n\n"
            
            if sell_signals:
                for i, signal in enumerate(sell_signals[:10], 1):
                    symbol = signal.get('symbol', '')
                    price = signal.get('price', 0)
                    confidence = signal.get('confidence', 0)
                    message += f"{i}. *{symbol}* - ₹{price:.2f} ({confidence:.0f}%)\n"
            else:
                message += "No sell signals available at the moment.\n"
            
            message += f"\n⏰ *Updated:* {datetime.now().strftime('%H:%M:%S')}"
            message += f"\n🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending sell list: {str(e)}")
            return False
    
    def _send_help_message(self) -> bool:
        """Send help message with available commands"""
        try:
            message = "*🤖 TRADING BOT HELP*\n\n"
            message += "*Available Commands:*\n\n"
            message += "/test - Test bot connection\n"
            message += "/status - Market status\n"
            message += "/buylist - Current buy signals\n"
            message += "/selllist - Current sell signals\n"
            message += "/watchlist - Current watchlist\n\n"
            message += "📱 *Professional Intraday Trading Assistant*\n"
            message += f"🤖 *Bot:* {self.bot_username}"
            
            return self.send_message(message)
            
        except Exception as e:
            print(f"Error sending help message: {str(e)}")
            return False
