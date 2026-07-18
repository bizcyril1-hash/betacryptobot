# Graph Report - C:\Users\saw_9\Desktop\BTC\scripts  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 10 nodes · 13 edges · 3 communities (2 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- analyze_bitcoin.py
- generate_analysis_report
- calculate_simple_moving_average

## God Nodes (most connected - your core abstractions)
1. `generate_analysis_report()` - 5 edges
2. `load_bitcoin_data()` - 3 edges
3. `calculate_simple_moving_average()` - 3 edges
4. `calculate_volatility()` - 3 edges
5. `main()` - 3 edges
6. `Charge les donnees Bitcoin depuis un fichier CSV.     Le fichier doit avoir les` - 1 edges
7. `Calcule la moyenne mobile simple sur une fenêtre donnée.` - 1 edges
8. `Calcule la volatilité (écart-type des rendements) sur une fenêtre donnée.` - 1 edges
9. `Génère un rapport d'analyse en remplissant le modèle avec les résultats.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `generate_analysis_report()` --calls--> `calculate_simple_moving_average()`  [EXTRACTED]
  analyze_bitcoin.py → analyze_bitcoin.py  _Bridges community 2 → community 1_
- `main()` --calls--> `generate_analysis_report()`  [EXTRACTED]
  analyze_bitcoin.py → analyze_bitcoin.py  _Bridges community 1 → community 0_

## Import Cycles
- None detected.

## Communities (3 total, 1 thin omitted)

### Community 0 - "analyze_bitcoin.py"
Cohesion: 0.67
Nodes (3): load_bitcoin_data(), main(), Charge les donnees Bitcoin depuis un fichier CSV.     Le fichier doit avoir les

### Community 1 - "generate_analysis_report"
Cohesion: 0.50
Nodes (4): calculate_volatility(), generate_analysis_report(), Calcule la volatilité (écart-type des rendements) sur une fenêtre donnée., Génère un rapport d'analyse en remplissant le modèle avec les résultats.

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `generate_analysis_report()` connect `generate_analysis_report` to `analyze_bitcoin.py`, `calculate_simple_moving_average`?**
  _High betweenness centrality (0.333) - this node is a cross-community bridge._
- **Why does `calculate_simple_moving_average()` connect `calculate_simple_moving_average` to `analyze_bitcoin.py`, `generate_analysis_report`?**
  _High betweenness centrality (0.222) - this node is a cross-community bridge._