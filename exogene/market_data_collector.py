"""
Market data collector for Betacryptobot
Collects OHLCV, volume, and order book data from cryptocurrency exchanges
"""

import ccxt
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional
import time
import duckdb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class MarketDataCollector:
    def __init__(self, db_path: str = "data/market_data.duckdb"):
        """Initialize the market data collector with exchange connections."""
        self.db_path = db_path
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # Only create directory if path includes a directory component
            os.makedirs(db_dir, exist_ok=True)
        self.conn = duckdb.connect(self.db_path)

        # Initialize exchanges
        self.exchanges = {}
        self._init_exchanges()

        # Create tables
        self._create_tables()

        logger.info("MarketDataCollector initialized")