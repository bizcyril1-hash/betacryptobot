#!/usr/bin/env python3
"""
Simple demonstration of the expanded exogenous data collection system
Shows how all the new collectors work together
"""

def demo_exogene_system():
    """Demonstrate the expanded exogenous data collection system"""
    print("=" * 70)
    print("BETACRYPTOBOT EXOGENOUS DATA COLLECTION SYSTEM")
    print("   Demonstrating the expanded data collection capabilities")
    print("=" * 70)

    try:
        # Import all collectors
        from exogene import (
            SocialSentimentCollector,
            MarketDataCollector,
            OnChainDataCollector,
            MacroDataCollector,
            AlternativeDataCollector,
            ExogenousDataOrchestrator
        )

        print("\n[OK] All exogenous data collectors imported successfully")

        # Show what each collector does
        print("\n" + "-" * 50)
        print("COLLECTOR OVERVIEW")
        print("-" * 50)

        print("\n1. Social Sentiment Collector (Existing)")
        print("   • Sources: Reddit, Twitter/X")
        print("   • Data: Posts, tweets, sentiment analysis")
        print("   • Storage: social_sentiment.duckdb (redemptions table)")

        print("\n2. Market Data Collector (NEW)")
        print("   • Sources: Cryptocurrency exchanges (Binance, Coinbase, etc.) via CCXT")
        print("   • Data: OHLCV, order book, trades, volume")
        print("   • Storage: market_data.duckdb (ohlcv_data, orderbook_snapshots, recent_trades tables)")

        print("\n3. On-Chain Data Collector (NEW)")
        print("   • Sources: Blockchain APIs (Etherscan, Blockchain.info), Web3")
        print("   • Data: Transaction counts, active addresses, exchange flows, whale movements")
        print("   • Storage: onchain_data.duckdb (ethereum_metrics, bitcoin_metrics, exchange_flows, whale_movements tables)")

        print("\n4. Macro Data Collector (NEW)")
        print("   • Sources: Yahoo Finance (indices, commodities, forex), FRED API (economic indicators)")
        print("   • Data: Market indices, commodities, forex rates, interest rates, economic indicators")
        print("   • Storage: macro_data.duckdb (market_indices, commodities, forex_rates, interest_rates, economic_indicators tables)")

        print("\n5. Alternative Data Collector (NEW)")
        print("   • Sources: Google Trends, Wikipedia, NewsAPI")
        print("   • Data: Search interest, article views, news sentiment and volume")
        print("   • Storage: alternative_data.duckdb (google_trends, wikipedia_views, news_data, social_volume tables)")

        print("\n6. Exogenous Data Orchestrator (NEW)")
        print("   • Purpose: Coordinates all collectors and provides unified interface")
        print("   • Features: Combined database views, scheduled collection, unified querying")
        print("   • Storage: exogene_combined.duckdb (with attached databases and views)")

        # Demonstrate basic usage
        print("\n" + "-" * 50)
        print("BASIC USAGE DEMONSTRATION")
        print("-" * 50)

        print("\n1. Individual Collector Usage:")
        print("   collector = MarketDataCollector()")
        print("   collector.collect_market_data(symbols=['BTC/USDT'], timeframes=['1h'])")

        print("\n2. Orchestrator Usage:")
        print("   orchestrator = ExogenousDataOrchestrator()")
        print("   results = orchestrator.collect_all_data()  # Collect from all sources")
        print("   data = orchestrator.get_data_for_analysis(lookback_hours=24)  # Get recent data")
        print("   orchestrator.close_all()  # Clean up")

        print("\n3. Integration with Existing Systems:")
        print("   • Social sentiment data feeds into existing analysis pipeline")
        print("   • All new data sources available to AI debate system (Grokcloud)")
        print("   • Unified querying through combined database views")
        print("   • Configurable collection frequencies for different data types")

        print("\n" + "=" * 70)
        print("SYSTEM READY FOR INTEGRATION")
        print("The expanded exogenous data collection system is now ready to")
        print("enhance the Betacryptobot's analysis capabilities!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"\n[ERROR] Error in demonstration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_exogene_system()
    exit(0 if success else 1)