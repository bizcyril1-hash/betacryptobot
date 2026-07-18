"""
Macro data collector for Betacryptobot
Collects macroeconomic indicators, traditional market data, and forex rates
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional
import time
import duckdb
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)