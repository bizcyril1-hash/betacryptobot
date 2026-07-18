"""
On-chain data collector for Betacryptobot
Collects blockchain and cryptocurrency network metrics
"""

import requests
import json
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any, Optional
import time
import duckdb
import os
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)