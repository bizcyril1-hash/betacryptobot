# Bitcoin Data Dictionary for Betacryptobot

This document describes the data fields collected and used by the Betacryptobot system, based on the project architecture and current implementation.

## Overview

Betacryptobot combines two analytical approaches:
1. **Promax-style exogenous analysis** - focuses on external data signals (market, on-chain, social, macro, alternative)
2. **Grokcloud-style debate system** - uses AI agents to debate and reduce bias in analysis

The data pipeline consists of:
1. Data collection from multiple sources
2. Preprocessing and feature engineering
3. Multi-agent analysis (analyst, critic, judge)
4. Risk management
5. Execution

## Data Categories

### 1. Market Data
*Source: Cryptocurrency exchanges (via CCXT or similar)*

| Column Name | Type | Description | Source |
|-------------|

(Note: This section is a placeholder for future implementation of market data collection. Based on the project description, market data should include price, volume, and order book information.) |
| symbol | STRING | Trading pair symbol (e.g., BTC-USDT) | Exchange ticker |
| timestamp | TIMESTAMP | Timestamp of the data point | Exchange timestamp |
| open | FLOAT | Opening price for the period | OHLCV data |
| high | FLOAT | Highest price for the period | OHLCV data |
| low | FLOAT | Lowest price for the period | OHLCV data |
| close | FLOAT | Closing price for the period | OHLCV data |
| volume | FLOAT | Trading volume (in base currency) | OHLCV data |
| bid_price | FLOAT | Best bid price (highest bid) | Order book |
| ask_price | FLOAT | Best ask price (lowest ask) | Order book |
| bid_volume | FLOAT | Volume at best bid | Order book |
| ask_volume | FLOAT | Volume at best ask | Order book |
| trade_count | INTEGER | Number of trades in period | Exchange trade data |
| vwap | FLOAT | Volume-weighted average price | Calculated from trades |

### 2. On-Chain Data
*Source: Blockchain explorers, node APIs, or specialized providers (e.g., Glassnode, CryptoQuant)*

| Column Name | Type | Description | Source |
|-------------|------|-------------|--------|
| timestamp | TIMESTAMP | Timestamp of the measurement | Blockchain timestamp |
| hash_rate | FLOAT | Network hash rate (TH/s) | Blockchain network |
| difficulty | FLOAT | Mining difficulty | Blockchain network |
| transaction_count | INTEGER | Number of transactions per day | Blockchain network |
| transaction_value_usd | FLOAT | Total USD value transferred per day | Blockchain network |
| active_addresses | INTEGER | Number of active addresses | Blockchain network |
| exchange_inflow | FLOAT | Bitcoin flowing into exchanges (BTC) | Exchange wallet monitoring |
| exchange_outflow | FLOAT | Bitcoin flowing out of exchanges (BTC) | Exchange wallet monitoring |
| miner_revenue | FLOAT | Total miner revenue (USD) | Blockchain rewards + fees |
| hash_ribbon | FLOAT | 30-day / 60-day hash rate moving average ratio | Derived from hash rate |
| nvt_ratio | FLOAT | Network Value to Transactions ratio | Market cap / transaction volume |
| s2f_model | FLOAT | Stock-to-Flow model value | Derived from supply and issuance |
| realized_cap | FLOAT | Realized market capitalization | Based on UTXO last moved price at last move |

### 3. Social Data
*Source: Social media platforms (Reddit, Twitter/X, forums, etc.) - Currently implemented*

#### 3.1 Raw Social Measurements (Stored in `redemptions` table)
| Column Name | Type | Description | Source |
|-------------|------|-------------|--------|
| id | VARCHAR (Primary Key) | Unique identifier for the post/tweet (platform-specific prefix) | Platform API |
| platform | VARCHAR | Source platform (e.g., 'reddit', 'twitter') | Platform API |
| created_at | TIMESTAMP | Original creation time of the post/tweet | Platform API |
| collected_at | TIMESTAMP | Timestamp when data was collected by bot | Collection time |
| raw_data | JSON | Platform-specific raw response data | Platform API |
| sentiment_score | DOUBLE | VADER sentiment compound score [-1, 1] | NLP processing |
| sentiment_label | VARCHAR | Sentiment category: 'positive', 'negative', 'neutral' | Derived from sentiment_score |
| text | TEXT | Truncated text content (max 500 chars) | Post/Tweet content |

#### 3.2 Platform-Specific Raw Data Fields (within `raw_data` JSON)
**For Reddit posts:**
- title: Post title
- selftext: Post body text
- score: Upvote count
- num_comments: Number of comments
- upvote_ratio: Percentage of upvotes
- subreddit: Subreddit name
- url: Post URL

**For Twitter/X posts:**
- text: Tweet text
- author_id: Author user ID
- metrics: Engagement metrics (retweet_count, reply_count, like_count, quote_count)
- language: Tweet language code
- query: Search query used to retrieve the tweet

#### 3.3 Aggregated Social Features (Derived)
| Column Name | Type | Description |
|-------------|------|-------------|
| social_volume | INTEGER | Number of posts/tweets collected in time window |
| sentiment_mean | DOUBLE | Average sentiment score |
| sentiment_std | DOUBLE | Standard deviation of sentiment scores |
| positive_ratio | FLOAT | Proportion of positive sentiments |
| negative_ratio | FLOAT | Proportion of negative sentiments |
| volume_weighted_sentiment | DOUBLE | Sentiment weighted by engagement (e.g., score, likes) |
| platform_distribution | JSON | Count of posts per platform |
| trending_topics | ARRAY | Frequently mentioned terms/hashtags |

### 4. Macro Data
*Source: Economic data providers (e.g., FRED, World Bank, TradingEconomics)*

| Column Name | Type | Description | Source |
|-------------|------|-------------|--------|
| timestamp | TIMESTAMP | Timestamp of the observation | Source publication date |
| interest_rate_usd | FLOAT | US Federal Funds Rate (%) | Federal Reserve |
| inflation_rate | FLOAT | CPI inflation rate (YoY %) | Bureau of Labor Statistics |
| gdp_growth | FLOAT | GDP growth rate (QoQ %) | Bureau of Economic Analysis |
| unemployment_rate | FLOAT | Unemployment rate (%) | Bureau of Labor Statistics |
| dollar_index | FLOAT | US Dollar Index (DXY) | ICE Futures US |
| gold_price | FLOAT | Gold price per ounce (USD) | Commodity markets |
| oil_price | FLOAT | Crude oil price per barrel (USD) | Commodity markets |
| vix_index | FLOAT | CBOE Volatility Index | CBOE |
| yield_spread_10y2y | FLOAT | 10-year minus 2-year Treasury yield spread | Treasury Department |
| consumer_confidence | INDEX | Consumer confidence index | Conference Board / University of Michigan |
| risk_on_off | CATEGORICAL | Market risk sentiment ('risk_on', 'risk_off', 'neutral') | Derived from multiple indicators |

### 5. Alternative Data
*Source: Alternative data providers (Google Trends, Wikipedia, GDELT, etc.)*

| Column Name | Type | Description | Source |
|-------------|------|-------------|--------|
| timestamp | TIMESTAMP | Timestamp of the observation | Source publication date |
| google_trends_btc | INTEGER | Relative search interest for "Bitcoin" (0-100) | Google Trends |
| google_trends_crypto | INTEGER | Relative search interest for "cryptocurrency" (0-100) | Google Trends |
| wiki_views_bitcoin | INTEGER | Daily Wikipedia page views for "Bitcoin" article | Wikipedia |
| wiki_views_cryptocurrency | INTEGER | Daily Wikipedia page views for "Cryptocurrency" article | Wikipedia |
| gdelt_event_count | INTEGER | Number of GDELT events related to Bitcoin/cryptocurrency | GDELT Project |
| gdelt_avg_tone | FLOAT | Average tone of GDELT events (-100 to +100, negative = negative tone) | GDELT Project |
| gdelt_num_sources | INTEGER | Number of unique sources reporting on Bitcoin/cryptocurrency | GDELT Project |
| twitter_hashtag_volume | INTEGER | Volume of tweets with #Bitcoin or #BTC | Twitter API |
| reddit_post_volume | INTEGER | Number of posts in cryptocurrency subreddits | Reddit API |
| google_search_volatility | FLOAT | Volatility of Google Trends search volume | Derived from Google Trends |
| wiki_edit_count | INTEGER | Number of edits to Bitcoin/Wikipedia cryptocurrency pages | Wikipedia API |

## 6. Preprocessing & Feature Engineering

After raw data collection, the following features are engineered:

### 6.1 Technical Features (from market data)
| Feature Name | Type | Description |
|--------------|------|-------------|
| returns_1h | FLOAT | Hourly log return |
| returns_24h | FLOAT | 24-hour log return |
| volatility_7d | FLOAT | 7-day rolling volatility of returns |
| rsi_14 | FLOAT | Relative Strength Index (14 periods) |
| macd | FLOAT | Moving Average Convergence Divergence |
| macd_signal | FLOAT | MACD signal line |
| bb_upper | FLOAT | Bollinger Bands upper band |
| bb_lower | FLOAT | Bollinger Bands lower band |
| bb_width | FLOAT | Bollinger Bands width |
| obv | FLOAT | On-Balance Volume |
| adi | FLOAT | Accumulation/Distribution Index |

### 6.2 Sentiment Features (from social data)
| Feature Name | Type | Description |
|--------------|------|-------------|
| sentiment_volume_weighted | DOUBLE | Sentiment score weighted by engagement metrics |
| sentiment_change_1h | FLOAT | Change in average sentiment over last hour |
| sentiment_change_24h | FLOAT | Change in average sentiment over last 24h |
| sentiment_dispersion | FLOAT | Standard deviation of sentiment across platforms |
| dominant_sentiment | VARCHAR | Most common sentiment label |
| sentiment_diversity_index | FLOAT | Entropy of sentiment distribution across categories |

### 6.3 Macro Features
| Feature Name | Type | Description |
|--------------|------|-------------|
| real_interest_rate | FLOAT | Interest rate minus inflation rate |
| yield_curve_slope | FLOAT | Difference between 10Y and 2Y yields |
| dollar_index_change | FLOAT | Daily change in DXY |
| commodities_index | FLOAT | Combined index of gold and oil prices |
| macro_surprise_index | FLOAT | Surprise index vs economist forecasts |

### 6.4 Alternative Data Features
| Feature Name | Type | Description |
|--------------|------|-------------|
| search_interest_change_7d | FLOAT | 7-day change in Google Trends search volume |
| wiki_velocity | FLOAT | Day-over-day change in Wikipedia views |
| gdelt_event_spike | BOOL | Flag for abnormal spike in GDELT event count |
| social_search_ratio | FLOAT | Ratio of social media volume to search interest |

### 6.5 Exogenous Factors (External Attention Measures)
| Feature Name | Type | Description |
|--------------|------|-------------|
| attention_index | FLOAT | Composite index of Google Trends, Wikipedia views, and social volume |
| news_volume | INTEGER | Number of news articles about Bitcoin (from news APIs) |
| regulatory_events | COUNT | Count of regulatory announcements affecting crypto |
| macro_event_flag | BOOL | Flag for major macroeconomic events (FOMC, CPI release, etc.) |

## 7. Multi-Agent Analysis Output

The debate system (Grokcloud style) produces the following output structure:

| Field Name | Type | Description |
|------------|------|-------------|
| topic | STRING | The debate topic (e.g., "Evaluation of current market context for Bitcoin") |
| rounds | ARRAY | Array of debate rounds, each containing arguments from analyst, critic, and judge |
| final_decision | OBJECT | Final decision from the judge agent |
| └─ decision | STRING | Recommended action: 'buy', 'sell', 'neutral', or 'no_decision' |
| └─ confidence | FLOAT | Confidence level in the decision (0.0 to 1.0) |
| └─ reasoning | TEXT | Explanation for the decision |
| └─ evidence | ARRAY | List of evidence/data points considered |

### 7.1 Debate Round Structure
| Field Name | Type | Description |
|------------|------|-------------|
| round_number | INTEGER | Sequential round number |
| arguments | ARRAY | Arguments from each agent in this round |
| └─ agent_role | STRING | Role: 'analyst', 'critic', or 'judge' |
| └─ content | TEXT | Argument content |
| └─ confidence | FLOAT | Confidence in the argument (0.0 to 1.0) |
| └─ timestamp | TIMESTAMP | Time the argument was generated |

## 8. Risk Management Outputs

| Field Name | Type Description |
| Let me correct the JSON format:
| Type | Description |
|------------|------|-------------|
| position_size_pct | FLOAT | Recommended position size as % of capital |
| stop_loss_price | FLOAT | Suggested stop-loss price level |
| take_profit_price | FLOAT | Suggested take-profit price level |
| var_95 | FLOAT | Value at Risk at 95% confidence level |
| expected_shortfall_95 | FLOAT | Expected Shortfall at 95% confidence level |
| volatility_estimate | FLOAT | Estimated volatility for position sizing |
| correlation_btc_market | FLOAT | Correlation between BTC and broader market |
| liquidation_risk_score | FLOAT | Score indicating liquidation risk (0-1) |

## 9. Execution Signals

| Field Name | Type | Description |
|------------|------|-------------|
| signal_timestamp | TIMESTAMP | When the signal was generated |
| signal_type | STRING | 'entry_long', 'entry_short', 'exit', 'hold' |
| signal_price | FLOAT | Price at which signal was generated |
| target_price | FLOAT | Target price for the position |
| stop_loss_price | FLOAT | Stop-loss price for the position |
| position_size | FLOAT | Position size in BTC |
| confidence | FLOAT | Confidence in the signal (0.0 to 1.0) |
| rationale | TEXT | Brief explanation of the signal rationale |
| strategy_version | STRING | Version of the strategy that generated the signal |

## Implementation Notes

1. **Currently Implemented**: Only social data collection (Reddit/Twitter) is implemented via `exogene/promax_social_sentiment.py`, storing data in DuckDB table `redemptions`.

2. **Planned Implementation**: Market, on-chain, macro, and alternative data collection modules are planned but not yet implemented.

3. **Storage**: All data is intended to be stored in DuckDB for efficient querying and analysis.

4. **Feature Engineering**: The preprocessing step will generate technical, sentiment, macro, alternative, and exogenous features from the raw data.

5. **Integration**: The engineered features feed into the multi-agent debate system (`grokcloud/debate_system.py`) which produces trading decisions.

6. **Extensibility**: The schema is designed to be extensible; new data sources can be added as new columns or tables.

## Usage

This data dictionary serves as:
- Reference for developers implementing data collection modules
- Documentation for data scientists building models
- Guide for maintaining and extending the Betacryptobot system
- Basis for defining data validation and quality checks