# Graph Report - C:\Users\saw_9\Desktop\BTC\exogene  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 62 nodes · 75 edges · 14 communities (8 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- manifest.json
- ._analyze_sentiment
- market_data_collector.py
- SocialSentimentCollector
- __init__.py
- exogene_orchestrator.py
- exogene_orchestrator.py
- macro_data_collector.py
- market_data_collector.py
- promax_social_sentiment.py
- .run_collection_cycle
- macro_data_collector.py
- onchain_data_collector.py
- .collect_twitter_tweets

## God Nodes (most connected - your core abstractions)
1. `SocialSentimentCollector` - 10 edges
2. `__init__.py` - 4 edges
3. `promax_social_sentiment.py` - 4 edges
4. `alternative_data_collector.py` - 4 edges
5. `exogene_orchestrator.py` - 4 edges
6. `macro_data_collector.py` - 4 edges
7. `market_data_collector.py` - 4 edges
8. `onchain_data_collector.py` - 4 edges
9. `MarketDataCollector` - 4 edges
10. `Exogene package for Betacryptobot - Exogenous data collection components.` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (14 total, 6 thin omitted)

### Community 0 - "manifest.json"
Cohesion: 0.15
Nodes (12): alternative_data_collector.py, ast_hash, mtime, semantic_hash, __init__.py, ast_hash, mtime, semantic_hash (+4 more)

### Community 1 - "._analyze_sentiment"
Cohesion: 0.40
Nodes (3): Any, Collecte des posts depuis les subreddits spécifiés.          Args:             s, Analyse le sentiment d'un texte et retourne le score et l'étiquette.

### Community 2 - "market_data_collector.py"
Cohesion: 0.40
Nodes (3): MarketDataCollector, Market data collector for Betacryptobot Collects OHLCV, volume, and order book d, Initialize the market data collector with exchange connections.

### Community 3 - "SocialSentimentCollector"
Cohesion: 0.50
Nodes (3): Initialise le collecteur avec les API disponibles., Crée les tables nécessaires si elles n'existent pas., SocialSentimentCollector

### Community 6 - "exogene_orchestrator.py"
Cohesion: 0.50
Nodes (4): exogene_orchestrator.py, ast_hash, mtime, semantic_hash

### Community 7 - "macro_data_collector.py"
Cohesion: 0.50
Nodes (4): macro_data_collector.py, ast_hash, mtime, semantic_hash

### Community 8 - "market_data_collector.py"
Cohesion: 0.50
Nodes (4): market_data_collector.py, ast_hash, mtime, semantic_hash

### Community 9 - "promax_social_sentiment.py"
Cohesion: 0.50
Nodes (4): promax_social_sentiment.py, ast_hash, mtime, semantic_hash

## Knowledge Gaps
- **21 isolated node(s):** `mtime`, `ast_hash`, `semantic_hash`, `mtime`, `ast_hash` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SocialSentimentCollector` connect `SocialSentimentCollector` to `._analyze_sentiment`, `__init__.py`, `exogene_orchestrator.py`, `.run_collection_cycle`, `.collect_twitter_tweets`?**
  _High betweenness centrality (0.171) - this node is a cross-community bridge._
- **Why does `promax_social_sentiment.py` connect `promax_social_sentiment.py` to `manifest.json`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **What connects `mtime`, `ast_hash`, `semantic_hash` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._