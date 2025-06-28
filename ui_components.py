"""
Enhanced UI components for Professional Intraday Trading Assistant
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
from config import TRADING_CONFIG

class UIComponents:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        if 'watchlist' not in st.session_state:
            from config import DEFAULT_WATCHLIST
            st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
        
        if 'selected_stock' not in st.session_state:
            st.session_state.selected_stock = 'RELIANCE'
        
        if 'scanning_active' not in st.session_state:
            st.session_state.scanning_active = False
        
        if 'alerts_enabled' not in st.session_state:
            st.session_state.alerts_enabled = True
        
        if 'telegram_connected' not in st.session_state:
            st.session_state.telegram_connected = False
        
        if 'current_timeframe' not in st.session_state:
            st.session_state.current_timeframe = TRADING_CONFIG['default_timeframe']
        
        if 'auto_refresh' not in st.session_state:
            st.session_state.auto_refresh = False
        
        if 'refresh_interval' not in st.session_state:
            st.session_state.refresh_interval = 15
    
    def create_metric_card(self, title: str, value: str, delta: str = None, delta_color: str = "normal") -> None:
        """Create a metric card with optional delta"""
        try:
            st.metric(
                label=title,
                value=value,
                delta=delta,
                delta_color=delta_color
            )
        except Exception as e:
            st.error(f"Error creating metric card: {str(e)}")
    
    def create_signal_card(self, signal_data: Dict[str, Any]) -> None:
        """Create a signal display card"""
        try:
            signal = signal_data.get('signal', 'HOLD')
            confidence = signal_data.get('confidence', 50)
            symbol = signal_data.get('symbol', 'UNKNOWN')
            price = signal_data.get('price', 0)
            
            # Determine card color based on signal
            if signal == 'BUY':
                card_color = "🟢"
                bg_color = "#d4edda"
            elif signal == 'SELL':
                card_color = "🔴"
                bg_color = "#f8d7da"
            else:
                card_color = "🔵"
                bg_color = "#e2e3f1"
            
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.markdown(f"## {card_color}")
                
                with col2:
                    st.markdown(f"**{symbol}** - {signal}")
                    st.caption(f"Price: ₹{price:.2f}")
                
                with col3:
                    st.metric("Confidence", f"{confidence:.0f}%")
        
        except Exception as e:
            st.error(f"Error creating signal card: {str(e)}")
    
    def create_progress_indicator(self, current: int, total: int, label: str = "Progress") -> None:
        """Create progress indicator"""
        try:
            if total > 0:
                progress = current / total
                st.progress(progress, text=f"{label}: {current}/{total}")
            else:
                st.info(f"{label}: No data")
        except Exception as e:
            st.error(f"Error creating progress indicator: {str(e)}")
    
    def create_data_table(self, data: pd.DataFrame, title: str = None, height: int = 400) -> None:
        """Create an enhanced data table"""
        try:
            if title:
                st.subheader(title)
            
            if data.empty:
                st.info("No data available")
                return
            
            # Configure column widths and formatting
            column_config = {}
            
            for col in data.columns:
                if col.lower() in ['price', 'entry price', 'exit price']:
                    column_config[col] = st.column_config.NumberColumn(
                        col,
                        format="₹%.2f"
                    )
                elif col.lower() in ['change %', 'p&l %']:
                    column_config[col] = st.column_config.NumberColumn(
                        col,
                        format="%.2f%%"
                    )
                elif col.lower() in ['volume']:
                    column_config[col] = st.column_config.NumberColumn(
                        col,
                        format="%d"
                    )
            
            st.dataframe(
                data,
                column_config=column_config,
                use_container_width=True,
                height=height
            )
        
        except Exception as e:
            st.error(f"Error creating data table: {str(e)}")
    
    def create_alert_notification(self, message: str, alert_type: str = "info") -> None:
        """Create alert notification"""
        try:
            if alert_type == "success":
                st.success(message)
            elif alert_type == "warning":
                st.warning(message)
            elif alert_type == "error":
                st.error(message)
            else:
                st.info(message)
        except Exception as e:
            st.error(f"Error creating alert: {str(e)}")
    
    def create_sidebar_filters(self) -> Dict[str, Any]:
        """Create comprehensive sidebar filters"""
        try:
            filters = {}
            
            with st.sidebar:
                st.header("🔧 Filters & Settings")
                
                # Stock selection
                st.subheader("📈 Stock Selection")
                
                # Search and add stocks
                new_stock = st.text_input("Add Stock to Watchlist", placeholder="Enter symbol (e.g., RELIANCE)")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("➕ Add", use_container_width=True):
                        if new_stock and new_stock.upper() not in st.session_state.watchlist:
                            st.session_state.watchlist.append(new_stock.upper())
                            st.success(f"Added {new_stock.upper()}")
                            st.rerun()
                
                with col2:
                    if st.button("🗑️ Clear All", use_container_width=True):
                        st.session_state.watchlist = []
                        st.success("Watchlist cleared")
                        st.rerun()
                
                # Display current watchlist
                if st.session_state.watchlist:
                    st.write(f"**Watchlist ({len(st.session_state.watchlist)} stocks):**")
                    
                    # Create remove buttons for each stock
                    for i, stock in enumerate(st.session_state.watchlist):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"{i+1}. {stock}")
                        with col2:
                            if st.button("❌", key=f"remove_{stock}", help=f"Remove {stock}"):
                                st.session_state.watchlist.remove(stock)
                                st.rerun()
                
                st.markdown("---")
                
                # Scan filters
                st.subheader("🔍 Scan Filters")
                
                filters['min_price'] = st.number_input(
                    "Min Price (₹)",
                    min_value=0.0,
                    value=TRADING_CONFIG['min_price_filter'],
                    step=5.0
                )
                
                filters['max_price'] = st.number_input(
                    "Max Price (₹)",
                    min_value=0.0,
                    value=TRADING_CONFIG['max_price_filter'],
                    step=100.0
                )
                
                filters['min_volume_ratio'] = st.slider(
                    "Min Volume Ratio",
                    min_value=0.5,
                    max_value=5.0,
                    value=1.0,
                    step=0.1
                )
                
                filters['rsi_min'] = st.slider(
                    "RSI Min",
                    min_value=0,
                    max_value=100,
                    value=20,
                    step=5
                )
                
                filters['rsi_max'] = st.slider(
                    "RSI Max",
                    min_value=0,
                    max_value=100,
                    value=80,
                    step=5
                )
                
                st.markdown("---")
                
                # Display settings
                st.subheader("🎨 Display Settings")
                
                filters['chart_height'] = st.slider(
                    "Chart Height",
                    min_value=400,
                    max_value=800,
                    value=600,
                    step=50
                )
                
                filters['refresh_interval'] = st.slider(
                    "Auto Refresh (seconds)",
                    min_value=5,
                    max_value=300,
                    value=30,
                    step=5
                )
                
                filters['max_results'] = st.slider(
                    "Max Results per Scan",
                    min_value=5,
                    max_value=50,
                    value=20,
                    step=5
                )
            
            return filters
        
        except Exception as e:
            st.error(f"Error creating sidebar filters: {str(e)}")
            return {}
    
    def create_status_indicators(self) -> None:
        """Create status indicators"""
        try:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Market status
                current_time = datetime.now()
                is_market_hours = (9 <= current_time.hour <= 15) and (current_time.weekday() < 5)
                
                if is_market_hours:
                    st.success("🟢 Market Open")
                else:
                    st.error("🔴 Market Closed")
            
            with col2:
                # Scanner status
                if st.session_state.scanning_active:
                    st.success("📡 Scanner Active")
                else:
                    st.info("📡 Scanner Inactive")
            
            with col3:
                # Telegram status
                if st.session_state.telegram_connected:
                    st.success("📱 Telegram Connected")
                else:
                    st.warning("📱 Telegram Disconnected")
            
            with col4:
                # Watchlist size
                watchlist_size = len(st.session_state.watchlist)
                st.info(f"📋 Watchlist: {watchlist_size} stocks")
        
        except Exception as e:
            st.error(f"Error creating status indicators: {str(e)}")
    
    def create_scan_results_display(self, scan_results: Dict[str, List[Dict]]) -> None:
        """Display scan results in organized format"""
        try:
            if not scan_results:
                st.info("No scan results available. Run a scan to see opportunities.")
                return
            
            # Create tabs for different scan types
            scan_types = list(scan_results.keys())
            
            if scan_types:
                tabs = st.tabs([scan_type.replace('_', ' ').title() for scan_type in scan_types])
                
                for i, (scan_type, results) in enumerate(scan_results.items()):
                    with tabs[i]:
                        if results:
                            st.write(f"Found {len(results)} opportunities")
                            
                            # Convert to DataFrame for better display
                            df_data = []
                            for result in results:
                                row = {
                                    'Symbol': result.get('symbol', ''),
                                    'Current Price': f"₹{result.get('current_price', result.get('price', 0)):.2f}",
                                    'Change %': f"{result.get('change_pct', 0):+.2f}%"
                                }
                                
                                # Add scan-specific columns
                                if 'volume_ratio' in result:
                                    row['Volume Ratio'] = f"{result['volume_ratio']:.1f}x"
                                if 'rsi' in result:
                                    row['RSI'] = f"{result['rsi']:.1f}"
                                if 'breakout_strength' in result:
                                    row['Breakout %'] = f"{result['breakout_strength']:.2f}%"
                                if 'gap_percentage' in result:
                                    row['Gap %'] = f"{result['gap_percentage']:+.2f}%"
                                
                                df_data.append(row)
                            
                            if df_data:
                                df = pd.DataFrame(df_data)
                                self.create_data_table(df, height=300)
                                
                                # Add action buttons
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    if st.button(f"📊 Analyze Top 5", key=f"analyze_{scan_type}"):
                                        st.info(f"Analyzing top 5 {scan_type} candidates...")
                                
                                with col2:
                                    if st.button(f"📱 Send to Telegram", key=f"telegram_{scan_type}"):
                                        st.info(f"Sending {scan_type} alerts to Telegram...")
                                
                                with col3:
                                    if st.button(f"📥 Export CSV", key=f"export_{scan_type}"):
                                        csv = df.to_csv(index=False)
                                        st.download_button(
                                            label="Download CSV",
                                            data=csv,
                                            file_name=f"{scan_type}_results.csv",
                                            mime="text/csv",
                                            key=f"download_{scan_type}"
                                        )
                        else:
                            st.info(f"No {scan_type.replace('_', ' ')} opportunities found.")
        
        except Exception as e:
            st.error(f"Error displaying scan results: {str(e)}")
    
    def create_performance_summary(self, metrics: Dict[str, Any]) -> None:
        """Create performance summary display"""
        try:
            if not metrics or metrics.get('total_trades', 0) == 0:
                st.info("No trading performance data available.")
                return
            
            st.subheader("📊 Trading Performance Summary")
            
            # Key metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                self.create_metric_card(
                    "Total Trades",
                    str(metrics.get('total_trades', 0))
                )
                
                self.create_metric_card(
                    "Win Rate",
                    f"{metrics.get('win_rate', 0):.1f}%"
                )
            
            with col2:
                total_pnl = metrics.get('total_pnl', 0)
                delta_color = "normal" if total_pnl >= 0 else "inverse"
                self.create_metric_card(
                    "Total P&L",
                    f"₹{total_pnl:,.0f}",
                    delta_color=delta_color
                )
                
                self.create_metric_card(
                    "Portfolio Return",
                    f"{metrics.get('total_pnl_percentage', 0):+.2f}%"
                )
            
            with col3:
                self.create_metric_card(
                    "Avg Win",
                    f"₹{metrics.get('avg_win', 0):,.0f}"
                )
                
                self.create_metric_card(
                    "Avg Loss",
                    f"₹{metrics.get('avg_loss', 0):,.0f}"
                )
            
            with col4:
                profit_factor = metrics.get('profit_factor', 0)
                if profit_factor == float('inf'):
                    pf_display = "∞"
                else:
                    pf_display = f"{profit_factor:.2f}"
                
                self.create_metric_card(
                    "Profit Factor",
                    pf_display
                )
                
                self.create_metric_card(
                    "Max Drawdown",
                    f"₹{metrics.get('max_drawdown', 0):,.0f}"
                )
            
            # Strategy breakdown
            strategy_performance = metrics.get('strategy_performance', {})
            if strategy_performance:
                st.subheader("📈 Performance by Strategy")
                
                strategy_data = []
                for strategy, stats in strategy_performance.items():
                    strategy_data.append({
                        'Strategy': strategy,
                        'Trades': stats['trades'],
                        'Win Rate': f"{stats['win_rate']:.1f}%",
                        'Total P&L': f"₹{stats['total_pnl']:,.0f}"
                    })
                
                if strategy_data:
                    df = pd.DataFrame(strategy_data)
                    self.create_data_table(df, height=200)
        
        except Exception as e:
            st.error(f"Error creating performance summary: {str(e)}")
    
    def create_trading_form(self) -> Dict[str, Any]:
        """Create trading form for manual entry"""
        try:
            st.subheader("📝 Add Trade")
            
            with st.form("trading_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    symbol = st.selectbox(
                        "Stock Symbol",
                        st.session_state.watchlist if st.session_state.watchlist else ['RELIANCE']
                    )
                    
                    trade_type = st.selectbox(
                        "Trade Type",
                        ["BUY", "SELL"]
                    )
                    
                    entry_price = st.number_input(
                        "Entry Price (₹)",
                        min_value=0.01,
                        value=100.0,
                        step=0.01
                    )
                    
                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        value=100,
                        step=1
                    )
                
                with col2:
                    strategy = st.selectbox(
                        "Strategy",
                        ["AI Signal", "Manual", "Breakout", "Reversal", "Momentum"]
                    )
                    
                    stop_loss = st.number_input(
                        "Stop Loss (₹)",
                        min_value=0.01,
                        value=95.0,
                        step=0.01
                    )
                    
                    take_profit = st.number_input(
                        "Take Profit (₹)",
                        min_value=0.01,
                        value=105.0,
                        step=0.01
                    )
                    
                    entry_date = st.datetime_input(
                        "Entry Date & Time",
                        value=datetime.now()
                    )
                
                notes = st.text_area(
                    "Notes",
                    placeholder="Enter trade notes, market conditions, etc."
                )
                
                # Calculate risk/reward
                if entry_price > 0 and stop_loss > 0 and take_profit > 0:
                    risk = abs(entry_price - stop_loss)
                    reward = abs(take_profit - entry_price)
                    rr_ratio = reward / risk if risk > 0 else 0
                    
                    st.info(f"Risk/Reward Ratio: {rr_ratio:.2f} (Risk: ₹{risk:.2f}, Reward: ₹{reward:.2f})")
                
                submitted = st.form_submit_button(
                    "💾 Add Trade",
                    type="primary",
                    use_container_width=True
                )
                
                if submitted:
                    return {
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
            
            return None
        
        except Exception as e:
            st.error(f"Error creating trading form: {str(e)}")
            return None
    
    def create_loading_spinner(self, message: str = "Loading...") -> None:
        """Create loading spinner with message"""
        try:
            with st.spinner(message):
                # This will be used with context manager
                pass
        except Exception as e:
            st.error(f"Error creating loading spinner: {str(e)}")
    
    def create_error_display(self, error_message: str, error_type: str = "error") -> None:
        """Create standardized error display"""
        try:
            if error_type == "warning":
                st.warning(f"⚠️ {error_message}")
            elif error_type == "info":
                st.info(f"ℹ️ {error_message}")
            else:
                st.error(f"❌ {error_message}")
        except Exception as e:
            st.error(f"Error displaying error: {str(e)}")
    
    def create_success_message(self, message: str) -> None:
        """Create success message display"""
        try:
            st.success(f"✅ {message}")
        except Exception as e:
            st.error(f"Error creating success message: {str(e)}")