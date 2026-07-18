"""
Alternative data collector for Betacryptobot
Collects alternative data sources like Google Trends, Wikipedia views, and news sentiment
"""

from pytrends.request import TrendReq
import wikipediaapi
import requests
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional
import time
import duckdb
import os
from dotenv import load_dot
import json

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)