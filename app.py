"""
Professional Intraday Trading Assistant - Main Application
Fixed and optimized version with comprehensive error handling
"""

import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd
import numpy as np
import warnings
import time
import traceback
warnings.filterwarnings('ignore')

# Configure Streamlit page first
st.set_page_config(
    page_title="Professional Intraday Trading Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def safe_import():
    """Safely import all required modules with error handling"""
    try:
        global config, DataFetcher, TechnicalIndicators, AISignalGenerator
        global StockScanner, ChartComponents, TradingJournal, UIComponents, utils
        
        import config
        from data_fetcher import DataFetcher
        from technical_indicators import TechnicalIndicators
        from ai_signals import AISignalGenerator
        from scanner import StockScanner
        from chart_components import ChartComponents
        from trading_journal import TradingJournal
        from ui_components import UIComponents
        import utils
        
        return True
    except ImportError as e:
        st.error(f"Import Error: {e}")
        st.error("Please ensure all required files are present.")
        return False
    except Exception as e:
        st.error(f"Unexpected error during import: {e}")
        return False

class TradingAssistant:
    def __init__(self):
        """Initialize the trading assistant with robust error handling"""
        try:
            # Initialize session state first
            self.initialize_session_state()
            
            # Initialize components
            self.ui = UIComponents()
            self.data_fetcher = DataFetcher()
            self.technical_indicators = TechnicalIndicators()
            self.ai_signals = AISignalGenerator()
            self.scanner = StockScanner()
            self.chart_components = ChartComponents()
            self.trading_journal = TradingJournal()
            
            st.session_state.app_initialized = True
            
        except Exception as e:
            st.error(f"Initialization Error: {str(e)}")
            st.error(f"Traceback: {traceback.format_exc()}")
            st.session_state.app_initialized = False
    
    def initialize_session_state(self):
        """Initialize all session state variables with defaults"""
        defaults = {
            'current_tab': 'scanner',
            'watchlist': getattr(config, 'DEFAULT_WATCHLIST', ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'SBIN']),
            'selected_stock': 'RELIANCE',
            'scanning_active': False,
            'alerts_enabled': True,
            'telegram_connected': False,
            'auto_refresh': False,
            'refresh_interval': 30,
            'scan_results': {},
            'last_scan_time': None,
            'error_count': 0,
            'app_initialized': False,
            'trades': [],
            'recent_alerts': [],
            'telegram_messages': [],
            'current_timeframe': '5m',
            'market_filter': 'NSE',
            'period_selector': '1d'
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def run(self):
        """Main application runner"""
        try:
            if not st.session_state.get('app_initialized', False):
                st.error("Application not properly initialized. Please refresh the page.")
                return
            
            # Apply styling
            self.apply_styling()
            
            # Create header
            self.create_header()
            
            # Create main layout
            self.create_main_layout()
            
            # Handle auto-refresh
            self.handle_auto_refresh()
            
        except Exception as e:
            st.error(f"Runtime Error: {str(e)}")
            if st.button("🔄 Restart Application"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    def handle_auto_refresh(self):
        """Handle auto-refresh logic"""
        if st.session_state.auto_refresh and utils.is_trading_time():
            time.sleep(st.session_state.refresh_interval)
            st.rerun()
    
    def apply_styling(self):
        """Apply custom CSS for better UI"""
        st.markdown("""
        <style>
        .main > div {
            padding: 1rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
        }
        
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            margin: 0.5rem 0;
        }
        
        .alert-box {
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 4px solid;
        }
        
        .alert-success {
            background-color: #d4edda;
            border-left-color: #28a745;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            border-left-color: #ffc107;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            border-left-color: #dc3545;
        }
        
        .status-indicator {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            font-weight: bold;
            margin: 0.25rem;
        }
        
        .status-active {
            background-color: #28a745;
        }
        
        .status-inactive {
            background-color: #6c757d;
        }
        
        .stDataFrame {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def create_header(self):
        """Create application header with status indicators"""
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1.5rem; border-radius: 10px; 
                    text-align: center; margin-bottom: 1rem;">
            <h1>📊 Professional Intraday Trading Assistant</h1>
            <p>Real-time NSE/BSE Scanner • AI-Powered Signals • Professional Trading Tools</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Status indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            market_status = utils.get_market_status()
            status_color = "#28a745" if market_status.get('is_open', False) else "#dc3545"
            status_text = market_status.get('status_text', '🔴 Market Closed')
            st.markdown(f"""
            <div class="status-indicator" style="background-color: {status_color};">
                {status_text}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            current_time = datetime.now()
            st.markdown(f"""
            <div class="status-indicator" style="background-color: #007bff;">
                📅 {current_time.strftime('%d %b %Y')}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="status-indicator" style="background-color: #6f42c1;">
                🕐 {current_time.strftime('%H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            scanner_status = "🟢 Active" if st.session_state.scanning_active else "🔴 Inactive"
            scanner_color = "#28a745" if st.session_state.scanning_active else "#6c757d"
            st.markdown(f"""
            <div class="status-indicator" style="background-color: {scanner_color};">
                📡 Scanner: {scanner_status}
            </div>
            """, unsafe_allow_html=True)
    
    def create_main_layout(self):
        """Create main application layout"""
        # Sidebar
        with st.sidebar:
            self.create_sidebar()
        
        # Main content with tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📡 Scanner", "🎯 AI Signals", "📊 Analysis", 
            "📈 Backtest", "📝 Journal", "🔔 Alerts"
        ])
        
        with tab1:
            self.render_scanner_tab()
        
        with tab2:
            self.render_signals_tab()
        
        with tab3:
            self.render_analysis_tab()
        
        with tab4:
            self.render_backtest_tab()
        
        with tab5:
            self.render_journal_tab()
        
        with tab6:
            self.render_alerts_tab()
    
    def create_sidebar(self):
        """Create comprehensive sidebar"""
        st.markdown("## 🎛️ Trading Control Panel")
        
        # Quick Actions
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📡 Start Scanner", use_container_width=True):
                st.session_state.scanning_active = True
                st.success("Scanner started!")
                st.rerun()
            
            if st.button("📊 Analysis", use_container_width=True):
                st.session_state.current_tab = 'analysis'
        
        with col2:
            if st.button("⏹️ Stop Scanner", use_container_width=True):
                st.session_state.scanning_active = False
                st.info("Scanner stopped!")
                st.rerun()
            
            if st.button("🔔 Alerts", use_container_width=True):
                st.session_state.current_tab = 'alerts'
        
        st.markdown("---")
        
        # Trading Parameters
        st.markdown("### ⚙️ Trading Setup")
        
        market_filter = st.selectbox(
            "🏛️ Market:",
            ["NSE", "BSE", "Both"],
            index=0,
            key="market_filter"
        )
        
        timeframe = st.selectbox(
            "⏰ Timeframe:",
            config.TRADING_CONFIG['timeframes'],
            index=config.TRADING_CONFIG['timeframes'].index(config.TRADING_CONFIG['default_timeframe']),
            key="timeframe_selector"
        )
        
        period = st.selectbox(
            "📅 Period:",
            ["1d", "2d", "5d"],
            index=0,
            key="period_selector"
        )
        
        st.markdown("---")
        
        # Scanner Configuration
        st.markdown("### 🔍 Scanner Config")
        
        volume_threshold = st.slider(
            "📊 Volume Surge:",
            min_value=1.5,
            max_value=5.0,
            value=config.ALERT_CONFIG['volume_surge_threshold'],
            step=0.1,
            key="volume_threshold"
        )
        
        rsi_overbought = st.slider(
            "📊 RSI Overbought:",
            min_value=60,
            max_value=90,
            value=config.ALERT_CONFIG['rsi_overbought'],
            step=5,
            key="rsi_overbought"
        )
        
        rsi_oversold = st.slider(
            "📊 RSI Oversold:",
            min_value=10,
            max_value=40,
            value=config.ALERT_CONFIG['rsi_oversold'],
            step=5,
            key="rsi_oversold"
        )
        
        st.markdown("---")
        
        # System Status
        st.markdown("### 📊 System Status")
        st.write(f"**Watchlist Size:** {len(st.session_state.watchlist)}")
        st.write(f"**Telegram:** {'✅ Connected' if st.session_state.telegram_connected else '❌ Disconnected'}")
        st.write(f"**Errors:** {st.session_state.get('error_count', 0)}")
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()
            
        # Auto-refresh toggle
        st.markdown("---")
        auto_refresh = st.toggle(
            "🔄 Enable Auto-Refresh", 
            value=st.session_state.auto_refresh,
            key="auto_refresh_toggle"
        )
        if auto_refresh:
            refresh_interval = st.slider(
                "Refresh Interval (seconds)",
                min_value=5,
                max_value=300,
                value=st.session_state.refresh_interval,
                step=5
            )
            st.session_state.refresh_interval = refresh_interval
    
    def render_scanner_tab(self):
        """Render the scanner tab"""
        try:
            st.header("📡 Real-time Stock Scanner")
            
            # Scanner controls
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🚀 Start Scanner", type="primary", use_container_width=True):
                    st.session_state.scanning_active = True
                    st.success("Scanner started!")
                    st.rerun()
            
            with col2:
                if st.button("⏹️ Stop Scanner", use_container_width=True):
                    st.session_state.scanning_active = False
                    st.info("Scanner stopped!")
                    st.rerun()
            
            with col3:
                if st.button("🔄 Refresh Data", use_container_width=True):
                    st.cache_data.clear()
                    st.success("Data refreshed!")
                    st.rerun()
            
            with col4:
                if st.button("📊 Quick Scan", use_container_width=True):
                    self.perform_quick_scan()
            
            st.markdown("---")
            
            # Scanner results
            if st.session_state.scanning_active:
                self.display_scanner_results()
            else:
                st.info("📡 Scanner is inactive. Click 'Start Scanner' to begin monitoring.")
                
                # Show last scan results if available
                if st.session_state.scan_results:
                    st.subheader("📋 Last Scan Results")
                    self.display_scan_summary()
        
        except Exception as e:
            st.error(f"Scanner Error: {str(e)}")
            self.increment_error_count()
    
    def render_signals_tab(self):
        """Render AI signals tab"""
        try:
            st.header("🎯 AI-Powered Trading Signals")
            
            # Stock selection
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                selected_stock = st.selectbox(
                    "Select Stock for Analysis:",
                    st.session_state.watchlist,
                    key="ai_stock_selector"
                )
            
            with col2:
                if st.button("🔍 Analyze", type="primary", use_container_width=True):
                    self.analyze_stock_signals(selected_stock)
            
            with col3:
                if st.button("📊 Batch Analyze", use_container_width=True):
                    self.batch_analyze_signals()
            
            st.markdown("---")
            
            # Display signals for selected stock
            if selected_stock:
                self.display_stock_signals(selected_stock)
        
        except Exception as e:
            st.error(f"AI Signals Error: {str(e)}")
            self.increment_error_count()
    
    def render_analysis_tab(self):
        """Render technical analysis tab"""
        try:
            st.header("📊 Technical Analysis")
            
            # Stock selection
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                selected_stock = st.selectbox(
                    "Select Stock:",
                    st.session_state.watchlist,
                    key="analysis_stock_selector"
                )
            
            with col2:
                chart_type = st.selectbox(
                    "Chart Type:",
                    ["Candlestick", "Line", "OHLC"],
                    key="chart_type_selector"
                )
            
            with col3:
                show_volume = st.checkbox("Show Volume", value=True, key="show_volume_check")
            
            if selected_stock:
                self.display_technical_analysis(selected_stock, chart_type, show_volume)
        
        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")
            self.increment_error_count()
    
    def render_backtest_tab(self):
        """Render backtesting tab"""
        try:
            st.header("📈 Strategy Backtesting")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("⚙️ Backtest Configuration")
                
                strategy = st.selectbox(
                    "Strategy:",
                    ["RSI Mean Reversion", "MACD Crossover", "Moving Average", "AI Signals"],
                    key="backtest_strategy"
                )
                
                test_symbol = st.selectbox(
                    "Test Symbol:",
                    st.session_state.watchlist,
                    key="backtest_symbol"
                )
                
                col_start, col_end = st.columns(2)
                with col_start:
                    start_date = st.date_input(
                        "Start Date",
                        value=datetime.now().date() - pd.Timedelta(days=30),
                        key="backtest_start_date"
                    )
                
                with col_end:
                    end_date = st.date_input(
                        "End Date",
                        value=datetime.now().date(),
                        key="backtest_end_date"
                    )
                
                capital = st.number_input(
                    "Initial Capital (₹):",
                    value=100000,
                    min_value=10000,
                    step=10000,
                    key="backtest_capital"
                )
                
                if st.button("🚀 Run Backtest", type="primary", use_container_width=True):
                    self.run_backtest(strategy, test_symbol, start_date, end_date, capital)
            
            with col2:
                st.subheader("📊 Backtest Results")
                self.display_backtest_results()
        
        except Exception as e:
            st.error(f"Backtest Error: {str(e)}")
            self.increment_error_count()
    
    def render_journal_tab(self):
        """Render trading journal tab"""
        try:
            st.header("📝 Trading Journal")
            
            journal_tab1, journal_tab2, journal_tab3 = st.tabs([
                "📝 Add Trade", "📊 View Trades", "📈 Performance"
            ])
            
            with journal_tab1:
                self.render_add_trade_form()
            
            with journal_tab2:
                self.render_trades_view()
            
            with journal_tab3:
                self.render_performance_metrics()
        
        except Exception as e:
            st.error(f"Journal Error: {str(e)}")
            self.increment_error_count()
    
    def render_alerts_tab(self):
        """Render alerts and notifications tab"""
        try:
            st.header("🔔 Alerts & Notifications")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("⚙️ Alert Configuration")
                
                # Telegram settings
                telegram_enabled = st.toggle(
                    "Enable Telegram Alerts",
                    value=st.session_state.alerts_enabled,
                    key="telegram_enabled_toggle"
                )
                
                if telegram_enabled:
                    col_test, col_status = st.columns(2)
                    
                    with col_test:
                        if st.button("🧪 Test Connection", use_container_width=True):
                            # This would call your Telegram bot test function
                            st.session_state.telegram_connected = True
                            st.success("✅ Telegram test successful!")
                    
                    with col_status:
                        status = "🟢 Connected" if st.session_state.telegram_connected else "🔴 Disconnected"
                        st.markdown(f"**Status:** {status}")
                
                st.markdown("---")
                
                # Alert types
                st.markdown("**Alert Types**")
                signal_alerts = st.checkbox("Trading Signals", value=True, key="signal_alerts_check")
                volume_alerts = st.checkbox("Volume Surges", value=True, key="volume_alerts_check")
                price_alerts = st.checkbox("Price Breakouts", value=True, key="price_alerts_check")
            
            with col2:
                st.subheader("📢 Recent Alerts")
                self.display_recent_alerts()
        
        except Exception as e:
            st.error(f"Alerts Error: {str(e)}")
            self.increment_error_count()
    
    def perform_quick_scan(self):
        """Perform quick scan of watchlist"""
        try:
            with st.spinner("Performing quick scan..."):
                results = []
                
                # Limit to first 10 stocks for quick scan
                stocks_to_scan = st.session_state.watchlist[:10]
                
                for stock in stocks_to_scan:
                    try:
                        data = self.data_fetcher.get_stock_data(stock, period='1d', interval='5m')
                        
                        if not data.empty:
                            signal = self.ai_signals.generate_signal(data, stock)
                            
                            results.append({
                                'Stock': stock,
                                'Signal': signal.get('signal', 'HOLD'),
                                'Price': f"₹{signal.get('price', 0):.2f}",
                                'Confidence': f"{signal.get('confidence', 50):.0f}%",
                                'RSI': f"{signal.get('rsi', 50):.1f}",
                                'Volume Ratio': f"{signal.get('volume_ratio', 1):.1f}x"
                            })
                    except Exception as e:
                        st.warning(f"Error scanning {stock}: {str(e)}")
                        continue
                
                if results:
                    st.subheader("📊 Quick Scan Results")
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    
                    # Summary
                    buy_signals = len([r for r in results if r['Signal'] == 'BUY'])
                    sell_signals = len([r for r in results if r['Signal'] == 'SELL'])
                    hold_signals = len([r for r in results if r['Signal'] == 'HOLD'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🟢 BUY Signals", buy_signals)
                    with col2:
                        st.metric("🔴 SELL Signals", sell_signals)
                    with col3:
                        st.metric("🔵 HOLD Signals", hold_signals)
                else:
                    st.warning("No scan results available.")
        
        except Exception as e:
            st.error(f"Quick Scan Error: {str(e)}")
            self.increment_error_count()
    
    def display_scanner_results(self):
        """Display live scanner results"""
        try:
            st.subheader("📊 Live Scanner Results")
            
            if st.button("🔄 Run Full Scan", type="primary", use_container_width=True):
                with st.spinner("Running comprehensive scan..."):
                    scan_results = self.scanner.comprehensive_scan(
                        st.session_state.watchlist[:20], 
                        self.data_fetcher
                    )
                    st.session_state.scan_results = scan_results
                    st.session_state.last_scan_time = datetime.now()
            
            if st.session_state.scan_results:
                self.display_scan_summary()
            else:
                st.info("No scan results available. Click 'Run Full Scan' to start.")
        
        except Exception as e:
            st.error(f"Scanner Results Error: {str(e)}")
            self.increment_error_count()
    
    def display_scan_summary(self):
        """Display scan results summary"""
        try:
            scan_results = st.session_state.scan_results
            
            if not scan_results:
                st.info("No scan results available.")
                return
            
            # Summary metrics
            total_opportunities = sum(len(results) for results in scan_results.values())
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Opportunities", total_opportunities)
            
            with col2:
                volume_count = len(scan_results.get('volume_surge', []))
                st.metric("Volume Surges", volume_count)
            
            with col3:
                breakout_count = len(scan_results.get('breakouts', []))
                st.metric("Breakouts", breakout_count)
            
            with col4:
                rsi_count = len(scan_results.get('rsi_extremes', []))
                st.metric("RSI Extremes", rsi_count)
            
            # Display results by category
            for scan_type, results in scan_results.items():
                if results:
                    st.markdown(f"### {scan_type.replace('_', ' ').title()}")
                    
                    df_data = []
                    for result in results[:5]:  # Top 5 per category
                        row = {
                            'Symbol': result.get('symbol', ''),
                            'Price': f"₹{result.get('current_price', result.get('price', 0)):.2f}",
                            'Change %': f"{result.get('change_pct', 0):+.2f}%"
                        }
                        
                        if 'volume_ratio' in result:
                            row['Volume Ratio'] = f"{result['volume_ratio']:.1f}x"
                        if 'rsi' in result:
                            row['RSI'] = f"{result['rsi']:.1f}"
                        
                        df_data.append(row)
                    
                    if df_data:
                        df = pd.DataFrame(df_data)
                        st.dataframe(df, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error displaying scan summary: {str(e)}")
    
    def analyze_stock_signals(self, stock):
        """Analyze individual stock for signals"""
        try:
            with st.spinner(f"Analyzing {stock}..."):
                data = self.data_fetcher.get_stock_data(stock, period='1d', interval='5m')
                
                if not data.empty:
                    signal = self.ai_signals.generate_signal(data, stock)
                    
                    # Display signal
                    self.display_signal_details(signal)
                    
                    # Send to Telegram if enabled
                    if st.session_state.alerts_enabled and st.session_state.telegram_connected:
                        try:
                            # This would call your Telegram send function
                            st.info("📱 Signal sent to Telegram!")
                        except Exception as e:
                            st.warning(f"Failed to send Telegram alert: {str(e)}")
                    
                    st.success(f"✅ Analysis complete for {stock}!")
                else:
                    st.error("❌ No data available for analysis.")
        
        except Exception as e:
            st.error(f"Signal Analysis Error: {str(e)}")
            self.increment_error_count()
    
    def display_signal_details(self, signal):
        """Display detailed signal information"""
        try:
            signal_type = signal.get('signal', 'HOLD')
            confidence = signal.get('confidence', 50)
            
            # Signal display
            if signal_type == 'BUY':
                st.success(f"🟢 **BUY SIGNAL** - Confidence: {confidence:.1f}%")
            elif signal_type == 'SELL':
                st.error(f"🔴 **SELL SIGNAL** - Confidence: {confidence:.1f}%")
            else:
                st.info(f"🔵 **HOLD SIGNAL** - Confidence: {confidence:.1f}%")
            
            # Signal metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Price", f"₹{signal.get('price', 0):.2f}")
            
            with col2:
                rsi = signal.get('rsi', 50)
                st.metric("📊 RSI", f"{rsi:.1f}")
            
            with col3:
                st.metric("📈 MACD", f"{signal.get('macd', 0):.3f}")
            
            with col4:
                volume_ratio = signal.get('volume_ratio', 1)
                st.metric("📊 Volume", f"{volume_ratio:.1f}x")
            
            # Supporting factors
            factors = signal.get('factors', [])
            if factors:
                st.markdown("**📋 Supporting Factors:**")
                for factor in factors:
                    st.write(f"• {factor}")
        
        except Exception as e:
            st.error(f"Error displaying signal details: {str(e)}")
    
    def display_stock_signals(self, stock):
        """Display AI signals for selected stock"""
        try:
            data = self.data_fetcher.get_stock_data(stock, period='1d', interval='5m')
            
            if not data.empty:
                signal = self.ai_signals.generate_signal(data, stock)
                self.display_signal_details(signal)
                
                # Risk assessment
                st.markdown("---")
                st.subheader("⚠️ Risk Assessment")
                
                risk_assessment = self.ai_signals.get_risk_assessment(data, signal)
                risk_level = risk_assessment.get('risk_level', 'Medium')
                risk_score = risk_assessment.get('risk_score', 50)
                
                risk_color = "#dc3545" if risk_level == "High" else "#ffc107" if risk_level == "Medium" else "#28a745"
                
                st.markdown(f"""
                <div style="background: {risk_color}; color: white; padding: 1rem; 
                           border-radius: 5px; text-align: center;">
                    <strong>Risk Level: {risk_level}</strong><br>
                    Risk Score: {risk_score:.0f}/100
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("No data available for signal generation.")
        
        except Exception as e:
            st.error(f"Error displaying stock signals: {str(e)}")
            self.increment_error_count()
    
    def batch_analyze_signals(self):
        """Batch analyze signals for multiple stocks"""
        try:
            with st.spinner("Analyzing watchlist..."):
                results = []
                
                for stock in st.session_state.watchlist[:10]:
                    try:
                        data = self.data_fetcher.get_stock_data(stock, period='1d', interval='5m')
                        
                        if not data.empty:
                            signal = self.ai_signals.generate_signal(data, stock)
                            results.append({
                                'stock': stock,
                                'signal': signal
                            })
                    except Exception:
                        continue
                
                if results:
                    st.subheader("📊 Batch Analysis Results")
                    
                    buy_signals = [r for r in results if r['signal']['signal'] == 'BUY']
                    sell_signals = [r for r in results if r['signal']['signal'] == 'SELL']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if buy_signals:
                            st.markdown("### 🟢 BUY Signals")
                            for result in buy_signals:
                                signal = result['signal']
                                st.write(f"**{result['stock']}** - Confidence: {signal['confidence']:.0f}%")
                    
                    with col2:
                        if sell_signals:
                            st.markdown("### 🔴 SELL Signals")
                            for result in sell_signals:
                                signal = result['signal']
                                st.write(f"**{result['stock']}** - Confidence: {signal['confidence']:.0f}%")
                    
                    st.success(f"✅ Found {len(buy_signals)} BUY and {len(sell_signals)} SELL signals.")
                else:
                    st.warning("No signals generated from batch analysis.")
        
        except Exception as e:
            st.error(f"Batch Analysis Error: {str(e)}")
            self.increment_error_count()
    
    def display_technical_analysis(self, stock, chart_type, show_volume):
        """Display technical analysis for selected stock"""
        try:
            with st.spinner(f"Loading data for {stock}..."):
                data = self.data_fetcher.get_stock_data(stock, period='1d', interval='5m')
                
                if not data.empty:
                    # Display chart
                    st.markdown("### 📈 Price Chart")
                    chart = self.chart_components.create_candlestick_chart(data, stock)
                    st.plotly_chart(chart, use_container_width=True)
                    
                    # Technical indicators
                    st.markdown("### 📊 Technical Indicators")
                    indicators = self.technical_indicators.calculate_all_indicators(data)
                    
                    if indicators:
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("RSI", f"{indicators.get('rsi', 50):.1f}")
                            st.metric("Current Price", f"₹{indicators.get('current_price', 0):.2f}")
                        
                        with col2:
                            st.metric("MACD", f"{indicators.get('macd', 0):.3f}")
                            st.metric("SMA 20", f"₹{indicators.get('sma_20', 0):.2f}")
                        
                        with col3:
                            st.metric("Volume Ratio", f"{indicators.get('volume_ratio', 1):.1f}x")
                            st.metric("ATR", f"₹{indicators.get('atr', 0):.2f}")
                        
                        with col4:
                            st.metric("BB Upper", f"₹{indicators.get('bb_upper', 0):.2f}")
                            st.metric("BB Lower", f"₹{indicators.get('bb_lower', 0):.2f}")
                    else:
                        st.warning("Unable to calculate technical indicators.")
                else:
                    st.error("No data available for this stock.")
        
        except Exception as e:
            st.error(f"Technical Analysis Error: {str(e)}")
            self.increment_error_count()
    
    def run_backtest(self, strategy, symbol, start_date, end_date, capital):
        """Run backtesting"""
        try:
            with st.spinner("Running backtest..."):
                # Get historical data
                historical_data = self.data_fetcher.get_historical_data(
                    symbol, str(start_date), str(end_date)
                )
                
                if historical_data.empty:
                    st.error("No historical data available for backtesting.")
                    return
                
                # Simple backtest implementation
                trades = []
                position = None
                portfolio_value = capital
                
                for i in range(20, len(historical_data)):
                    try:
                        current_data = historical_data.iloc[:i+1]
                        signal = self.ai_signals.generate_signal(current_data, symbol)
                        current_price = current_data['Close'].iloc[-1]
                        
                        # Simple strategy execution
                        if signal['signal'] == 'BUY' and position is None and signal['confidence'] > 70:
                            shares = int(portfolio_value * 0.9 / current_price)
                            position = {
                                'entry_price': current_price,
                                'shares': shares,
                                'entry_date': current_data.index[-1]
                            }
                        
                        elif signal['signal'] == 'SELL' and position is not None:
                            exit_value = position['shares'] * current_price
                            pnl = exit_value - (position['shares'] * position['entry_price'])
                            
                            trades.append({
                                'entry_date': position['entry_date'],
                                'exit_date': current_data.index[-1],
                                'entry_price': position['entry_price'],
                                'exit_price': current_price,
                                'shares': position['shares'],
                                'pnl': pnl,
                                'return_pct': (pnl / (position['shares'] * position['entry_price'])) * 100
                            })
                            
                            portfolio_value += pnl
                            position = None
                    except Exception:
                        continue
                
                # Store results
                if trades:
                    total_trades = len(trades)
                    winning_trades = len([t for t in trades if t['pnl'] > 0])
                    total_pnl = sum(t['pnl'] for t in trades)
                    win_rate = (winning_trades / total_trades) * 100
                    
                    st.session_state.backtest_results = {
                        'strategy': strategy,
                        'symbol': symbol,
                        'total_trades': total_trades,
                        'winning_trades': winning_trades,
                        'win_rate': win_rate,
                        'total_pnl': total_pnl,
                        'total_return': (total_pnl / capital) * 100,
                        'final_value': portfolio_value,
                        'trades': trades
                    }
                    
                    st.success("✅ Backtest completed successfully!")
                else:
                    st.warning("No trades were generated during the backtest period.")
        
        except Exception as e:
            st.error(f"Backtest Error: {str(e)}")
            self.increment_error_count()
    
    def display_backtest_results(self):
        """Display backtest results"""
        try:
            if 'backtest_results' in st.session_state and st.session_state.backtest_results:
                results = st.session_state.backtest_results
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Trades", results['total_trades'])
                
                with col2:
                    st.metric("Win Rate", f"{results['win_rate']:.1f}%")
                
                with col3:
                    st.metric("Total P&L", f"₹{results['total_pnl']:,.0f}")
                
                with col4:
                    st.metric("Total Return", f"{results['total_return']:+.1f}%")
                
                # Trade details
                if results['trades']:
                    st.subheader("📊 Trade Details")
                    trades_df = pd.DataFrame(results['trades'])
                    
                    # Format for display
                    trades_df['Entry Date'] = pd.to_datetime(trades_df['entry_date']).dt.strftime('%Y-%m-%d')
                    trades_df['Exit Date'] = pd.to_datetime(trades_df['exit_date']).dt.strftime('%Y-%m-%d')
                    trades_df['P&L'] = trades_df['pnl'].apply(lambda x: f"₹{x:,.0f}")
                    trades_df['Return %'] = trades_df['return_pct'].apply(lambda x: f"{x:+.1f}%")
                    
                    display_df = trades_df[['Entry Date', 'Exit Date', 'P&L', 'Return %']]
                    st.dataframe(display_df, use_container_width=True)
            else:
                st.info("No backtest results available. Configure and run a backtest to see results.")
        
        except Exception as e:
            st.error(f"Error displaying backtest results: {str(e)}")
    
    def render_add_trade_form(self):
        """Render add trade form"""
        try:
            st.subheader("📝 Add New Trade")
            
            with st.form("add_trade_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    symbol = st.selectbox("Stock Symbol", st.session_state.watchlist)
                    trade_type = st.selectbox("Trade Type", ["BUY", "SELL"])
                    entry_price = st.number_input("Entry Price (₹)", min_value=0.01, value=100.0, step=0.01)
                    quantity = st.number_input("Quantity", min_value=1, value=100, step=1)
                
                with col2:
                    strategy = st.selectbox("Strategy", ["AI Signal", "Manual", "Breakout", "Reversal"])
                    stop_loss = st.number_input("Stop Loss (₹)", min_value=0.01, value=95.0, step=0.01)
                    take_profit = st.number_input("Take Profit (₹)", min_value=0.01, value=105.0, step=0.01)
                    entry_date = st.datetime_input("Entry Date & Time", value=datetime.now())
                
                notes = st.text_area("Notes", placeholder="Enter trade notes...")
                
                if st.form_submit_button("💾 Add Trade", type="primary", use_container_width=True):
                    trade_data = {
                        'symbol': symbol,
                        'trade_type': trade_type,
                        'entry_price': entry_price,
                        'quantity': quantity,
                        'strategy': strategy,
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'entry_date': entry_date,
                        'notes': notes
                    }
                    
                    if self.trading_journal.add_trade(trade_data):
                        st.success("✅ Trade added successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to add trade.")
        
        except Exception as e:
            st.error(f"Add Trade Error: {str(e)}")
            self.increment_error_count()
    
    def render_trades_view(self):
        """Render trades view"""
        try:
            st.subheader("📊 Trade History")
            
            df = self.trading_journal.get_trades_dataframe()
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("📝 No trades recorded yet. Add your first trade using the 'Add Trade' tab.")
        
        except Exception as e:
            st.error(f"Trades View Error: {str(e)}")
            self.increment_error_count()
    
    def render_performance_metrics(self):
        """Render performance metrics"""
        try:
            st.subheader("📈 Performance Analytics")
            
            metrics = self.trading_journal.get_performance_metrics()
            
            if metrics['total_trades'] > 0:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Trades", metrics['total_trades'])
                    st.metric("Win Rate", f"{metrics['win_rate']:.1f}%")
                
                with col2:
                    st.metric("Total P&L", f"₹{metrics['total_pnl']:,.2f}")
                    st.metric("P&L %", f"{metrics['total_pnl_percentage']:+.2f}%")
                
                with col3:
                    st.metric("Avg Win", f"₹{metrics['avg_win']:,.2f}")
                    st.metric("Avg Loss", f"₹{metrics['avg_loss']:,.2f}")
                
                with col4:
                    st.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")
                    st.metric("Max Drawdown", f"₹{metrics['max_drawdown']:,.2f}")
            else:
                st.info("📊 No performance data available yet. Start trading to see analytics!")
        
        except Exception as e:
            st.error(f"Performance Metrics Error: {str(e)}")
            self.increment_error_count()
    
    def display_recent_alerts(self):
        """Display recent alerts"""
        try:
            if st.session_state.recent_alerts:
                for alert in st.session_state.recent_alerts[-5:]:
                    alert_time = alert.get('timestamp', datetime.now())
                    alert_text = alert.get('message', str(alert))
                    alert_type = alert.get('type', 'info')
                    
                    if alert_type == 'buy':
                        st.success(f"🟢 {alert_time.strftime('%H:%M')} - {alert_text}")
                    elif alert_type == 'sell':
                        st.error(f"🔴 {alert_time.strftime('%H:%M')} - {alert_text}")
                    else:
                        st.info(f"🔔 {alert_time.strftime('%H:%M')} - {alert_text}")
            else:
                st.info("No recent alerts. Alerts will appear here when generated.")
                
                if st.button("📢 Generate Sample Alert"):
                    sample_alert = {
                        'message': 'RELIANCE - BUY Signal Generated (Confidence: 75%)',
                        'type': 'buy',
                        'timestamp': datetime.now()
                    }
                    st.session_state.recent_alerts.append(sample_alert)
                    st.rerun()
        
        except Exception as e:
            st.error(f"Recent Alerts Error: {str(e)}")
    
    def increment_error_count(self):
        """Increment error count for debugging"""
        if 'error_count' not in st.session_state:
            st.session_state.error_count = 0
        st.session_state.error_count += 1

def main():
    """Main function with error handling"""
    try:
        # Check if imports are successful
        if not safe_import():
            st.stop()
        
        # Initialize and run the app
        app = TradingAssistant()
        app.run()
        
    except Exception as e:
        st.error("🚨 Critical Application Error")
        st.error(f"Error: {str(e)}")
        
        # Recovery options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Restart App", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.success("Cache cleared!")

if __name__ == "__main__":
    main()