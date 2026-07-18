"""
Enhanced demonstration of exogenous data collection for Betacryptobot
Shows the expanded data collection capabilities beyond just social sentiment
"""

import sys
import os
from datetime import datetime
import json

# Add local directories to path for import
sys.path.append(os.path.join(os.path.dirname(__file__), 'exogene'))

def demo_comprehensive_exogene_collection():
    """Demonstrates comprehensive exogenous data collection (all data types)"""
    print("=" * 80)
    print("ENHANCED EXOGENOUS DATA COLLECTION DEMONSTRATION")
    print("   Combining multiple data sources for comprehensive crypto analysis")
    print("=" * 80)

    try:
        # Import the orchestrator
        from exogene_orchestrator import ExogenousDataOrchestrator

        print("\nInitializing Exogenous Data Orchestrator...")
        orchestrator = ExogenousDataOrchestrator(base_data_dir="data")

        print("\nStarting comprehensive data collection across all sources...")
        print("- Social sentiment (Reddit/Twitter)")
        print("- Market data (OHLCV, order book, trades)")
        print("- On-chain data (Ethereum/Bitcoin metrics)")
        print("- Macro data (indices, commodities, forex, economic indicators)")
        print("- Alternative data (Google Trends, Wikipedia, news)")

        # Run collection with limited scope for demo purposes
        results = orchestrator.collect_all_data(
            social_config={
                'reddit_limit': 20,  # Reduced for demo
                'twitter_max_results': 20
            },
            market_config={
                'symbols': ['BTC/USDT', 'ETH/USDT'],
                'timeframes': ['1h'],
                'exchanges': ['binance']  # Will use demo data if no API keys
            }
            # Other configs use defaults
        )

        print(f"\nData collection completed in {results['duration_seconds']:.2f} seconds")
        print("\nCollection Results Summary:")
        print("-" * 40)

        # Social results
        social_result = results.get('social', {})
        print(f"Social Sentiment: {social_result.get('records_collected', 0)} records "
              f"({social_result.get('status', 'unknown')})")

        # Market results
        market_result = results.get('market', {})
        print(f"Market Data: {market_result.get('ohlcv_records', 0)} OHLCV, "
              f"{market_result.get('orderbook_snapshots', 0)} order book, "
              f"{market_result.get('trade_records', 0)} trades "
              f"({market_result.get('status', 'unknown')})")

        # On-chain results
        onchain_result = results.get('onchain', {})
        print(f"On-Chain: {onchain_result.get('ethereum_records', 0)} ETH, "
              f"{onchain_result.get('bitcoin_records', 0)} BTC records "
              f"({onchain_result.get('status', 'unknown')})")

        # Macro results
        macro_result = results.get('macro', {})
        print(f"Macro Data: {macro_result.get('market_indices_records', 0)} indices, "
              f"{macro_result.get('commodities_records', 0)} commodities, "
              f"{macro_result.get('forex_records', 0)} forex, "
              f"{macro_result.get('economic_indicators_records', 0)} indicators "
              f"({macro_result.get('status', 'unknown')})")

        # Alternative results
        alt_result = results.get('alternative', {})
        print(f"Alternative Data: {alt_result.get('google_trends_records', 0)} trends, "
              f"{alt_result.get('wikipedia_records', 0)} Wikipedia, "
              f"{alt_result.get('news_records', 0)} news articles "
              f"({alt_result.get('status', 'unknown')})")

        # Demonstrate data retrieval for analysis
        print("\n" + "-" * 80)
        print("DEMONSTRATING DATA ACCESS FOR ANALYSIS")
        print("-" * 80)

        # Get recent social sentiment data
        recent_social = orchestrator.get_latest_data('social', limit=10)
        print(f"\nRecent Social Sentiment Samples ({len(recent_social)} records):")
        for i, record in enumerate(recent_social[:3]):  # Show first 3
            print(f"  {i+1}. [{record.get('platform', 'unknown').upper()}] "
                  f"{record.get('sentiment_label', 'unknown').upper()} "
                  f"({record.get('sentiment_score', 0):+.2f}): "
                  f"\"{str(record.get('text', ''))[:50]}...\"")

        # Get recent market data
        recent_market = orchestrator.get_latest_data('market', limit=5)
        print(f"\nRecent Market Data Samples ({len(recent_market)} records):")
        for i, record in enumerate(recent_market[:3]):
            print(f"  {i+1}. {record.get('symbol', 'unknown')} "
                  f"{report.get('timeframe', '1h')}: "
                  f"O:{record.get('open', 0):.2f} H:{record.get('high', 0):.2f} "
                  f"L:{record.get('low', 0):.2f} C:{record.get('close', 0):.2f} "
                  f"V:{record.get('volume', 0):.0f}")

        # Get on-chain data
        recent_eth = orchestrator.get_latest_data('ethereum', limit=3)
        print(f"\nRecent Ethereum Metrics Samples ({len(recent_eth)} records):")
        for i, record in enumerate(recent_eth):
            print(f"  {i+1}. Block {record.get('block_height', 0)} "
                  f"Tx: {record.get('transaction_count', 0):,} "
                  f"Gas Price: {record.get('gas_price_gwei', 0):.1f} gwei")

        # Get macro data
        recent_indices = orchestrator.get_latest_data('market_indices', limit=3)
        print(f"\nRecent Market Indices Samples ({len(recent_indices)} records):")
        for i, record in enumerate(recent_indices):
            print(f"  {i+1}. {record.get('name', 'unknown')}: "
                  f"{'${:,.2f}'.format(float(str(record.get('close', 0))))} "
                  f"({{:+.2f%%}})".format(
                      ((float(str(record.get('close', 0))) - float(str(record.get('open', 0)))) /
                       float(str(record.get('open', 1)))) if float(str(record.get('open', 0))) != 0 else 0
                  ))

        # Get alternative data
        recent_trends = orchestrator.get_latest_data('google_trends', limit=3)
        print(f"\nRecent Google Trends Samples ({len(recent_trends)} records):")
        for i, record in enumerate(recent_trends):
            print(f"  {i+1}. {record.get('keyword', 'unknown')}: "
                  f"{record.get('value', 0)} interest")

        recent_news = orchestrator.get_latest_data('news', limit=3)
        print(f"\nRecent News Samples ({len(recent_news)} records):")
        for i, record in enumerate(recent_news):
            print(f"  {i+1}. '{record.get('query', 'unknown')}' "
                  f"({record.get('article_count', 0)} articles, "
                  f"sentiment: {float(str(record.get('avg_sentiment', 0))):+.2f})")

        # Demonstrate integrated data access for analysis
        print("\n" + "-" * 80)
        print("INTEGRATED DATA ACCESS FOR AI ANALYSIS")
        print("-" * 80)

        # Get data from all sources for the last 6 hours for analysis
        analysis_data = orchestrator.get_data_for_analysis(lookback_hours=6)
        print(f"\nData available for AI analysis (last 6 hours):")
        for data_type, records in analysis_data.items():
            print(f"  {data_type}: {len(records)} records")

        # Clean up
        orchestrator.close_all()

        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETE")
        print("The exogenous data collection system is ready to feed")
        print("the AI debate system (Grokcloud) with comprehensive data!")
        print("=" * 80)

        return {
            "status": "success",
            "data_sources_collected": len([k for k in results.keys() if k not in ['start_time', 'end_time', 'duration_seconds'] and results[k].get('status') == 'success']),
            "total_records": sum([
                results.get('social', {}).get('records_collected', 0),
                results.get('market', {}).get('ohlcv_records', 0) +
                results.get('market', {}).get('orderbook_snapshots', 0) +
                results.get('market', {}).get('trade_records', 0),
                results.get('onchain', {}).get('ethereum_records', 0) +
                results.get('onchain', {}).get('bitcoin_records', 0),
                results.get('macro', {}).get('market_indices_records', 0) +
                results.get('macro', {}).get('commodities_records', 0) +
                results.get('macro', {}).get('forex_records', 0) +
                results.get('macro', {}).get('economic_indicators_records', 0),
                results.get('alternative', {}).get('google_trends_records', 0) +
                results.get('alternative', {}).get('wikipedia_records', 0) +
                results.get('alternative', {}).get('news_records', 0)
            ])
        }

    except ImportError as e:
        print(f"WARNING: Could not import exogenous data collector: {e}")
        print("Using simplified demonstration...")

        # Fallback to original demo
        return demo_original_social_only()

    except Exception as e:
        print(f"ERROR during demonstration: {e}")
        return {"status": "error", "message": str(e)}


def demo_original_social_only():
    """Original social-only demonstration as fallback"""
    print("\nRunning original social sentiment only demonstration...")

    try:
        from promax_social_sentiment import SocialSentimentCollector

        print("Initializing social sentiment collector...")
        collector = SocialSentimentCollector()

        print("Simulating social data collection (API keys not configured)...")

        # Create demonstration data
        demo_data = [
            {
                "id": "demo_reddit_1",
                "platform": "reddit",
                "created_at": datetime.now(),
                "collected_at": datetime.now(),
                "raw_data": '{"title": "Bitcoin shows strong recovery signs", "selftext": "BTC up 5% today as institutional adoption grows", "score": 1250, "num_comments": 89, "upvote_ratio": 0.87, "subreddit": "CryptoCurrency", "url": "https://reddit.com/r/CryptoCurrency/demo"}',
                "sentiment_score": 0.65,
                "sentiment_label": "positive",
                "text": "Bitcoin shows strong recovery signs BTC up 5% today as institutional adoption grows"
            },
            {
                "id": "demo_twitter_1",
                "platform": "twitter",
                "created_at": datetime.now(),
                "collected_at": datetime.now(),
                "raw_data": '{"text": "Concerned about BTC volatility amid regulatory uncertainty", "author_id": "12345", "metrics": {"retweet_count": 42, "reply_count": 18, "like_count": 156}, "language": "en"}',
                "sentiment_score": -0.35,
                "sentiment_label": "negative",
                "text": "Concerned about BTC volatility amid regulatory uncertainty"
            }
        ]

        print(f"[OK] Simulated collection of {len(demo_data)} social data items")
        print("  - Positive sentiment: 1 items")
        print("  - Negative sentiment: 1 items")
        print("  - Platforms: Reddit (1), Twitter (1)")

        print("\nSummary of collected sentiments:")
        for item in demo_data:
            print(f"  [{item['platform'].upper()}] {item['sentiment_label'].upper()} ({item['sentiment_score']:+.2f})")
            print(f"    \"{item['text'][:50]}...\"")

        collector.close()

        return {
            "status": "success",
            "data_type": "social_only",
            "records_collected": len(demo_data)
        }

    except ImportError as e:
        print(f"ERROR: Could not import SocialSentimentCollector: {e}")
        return {"status": "error", "message": "Social sentiment collector not available"}


def demo_integration():
    """Main demonstration function"""
    print("BETACRYPTOBOT ENHANCED EXOGENOUS DATA DEMONSTRATION")
    print("   Advanced data collection for cryptocurrency analysis\n")

    try:
        result = demo_comprehensive_exogene_collection()

        print("\nEXECUTION SUMMARY:")
        print(f"   Status: {result.get('status', 'unknown')}")
        if 'data_sources_collected' in result:
            print(f"   Data sources successfully collected: {result['data_sources_collected']}/5")
        if 'total_records' in result:
            print(f"   Total data records collected: {result['total_records']}")

        return result

    except Exception as e:
        print(f"\nERROR: {e}")
        print("   Please verify all modules are correctly installed.")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    try:
        result = demo_integration()
        print(f"\nDemo completed with status: {result.get('status', 'unknown')}")
    except Exception as e:
        print(f"\nFailed to run demonstration: {e}")
        sys.exit(1)