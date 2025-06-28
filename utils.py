"""
Utility functions for the Professional Intraday Trading Assistant
"""

import pandas as pd
import numpy as np
import json
import csv
import os
from datetime import datetime, time, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
import streamlit as st
import warnings
warnings.filterwarnings('ignore')

def is_trading_time() -> bool:
    """Check if current time is within NSE trading hours (IST)"""
    current = datetime.now().time()
    return (
        current >= time(9, 15) 
        and current <= time(15, 30)
        and datetime.today().weekday() < 5  # Monday to Friday
    )

def get_market_status() -> Dict[str, Any]:
    """Get current market status"""
    try:
        current_time = datetime.now()
        is_open = is_trading_time()
        
        return {
            'is_open': is_open,
            'status_text': '🟢 Market Open' if is_open else '🔴 Market Closed'
        }
        
    except Exception:
        return {
            'is_open': False,
            'status_text': '⚠️ Status Unknown'
        }