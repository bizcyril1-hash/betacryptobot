"""
Exogenous Data Orchestrator for Betacryptobot
Coordinates all data collectors and provides a unified interface
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import time
import duckdb
import os

# Import all collectors
from .promax_social_sentiment import SocialSentimentCollector
from .market_data_collector import MarketDataCollector
from .onchain_data_collector import OnChainDataCollector
from .macro_data_collector import MacroDataCollector
from .alternative_data_collector import AlternativeDataCollector

logger = logging.getLogger(__name__)