# Graph Report - C:\Users\saw_9\Desktop\BTC\grokcloud  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 34 nodes · 49 edges · 5 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- DebateEngine
- DebateArgument
- debate_system.py
- DebateAgent
- .conduct_debate

## God Nodes (most connected - your core abstractions)
1. `DebateEngine` - 11 edges
2. `DebateArgument` - 6 edges
3. `DebateAgent` - 5 edges
4. `example_usage()` - 4 edges
5. `AgentRole` - 3 edges
6. `DebateRound` - 3 edges
7. `Grokcloud package for Betacryptobot - AI debate system components.` - 1 edges
8. `Système de débat entre IA pour Betacryptobot Inspiré de Grokcloud : système de v` - 1 edges
9. `Représente un argument dans le débat` - 1 edges
10. `Représente une ronde de débat` - 1 edges

## Surprising Connections (you probably didn't know these)
- `example_usage()` --calls--> `DebateEngine`  [EXTRACTED]
  debate_system.py → debate_system.py  _Bridges community 0 → community 4_

## Import Cycles
- None detected.

## Communities (5 total, 0 thin omitted)

### Community 0 - "DebateEngine"
Cohesion: 0.28
Nodes (6): Any, DebateEngine, Génère la décision finale basée sur tous les rounds, Sauvegarde le résultat du débat dans un fichier JSON, Charge un débat précédemment sauvegardé, Moteur qui orchestre le débat entre les agents

### Community 1 - "DebateArgument"
Cohesion: 0.29
Nodes (4): DebateArgument, Génère un résumé de la ronde, Vérifie si un consensus a été atteint, Représente un argument dans le débat

### Community 2 - "debate_system.py"
Cohesion: 0.40
Nodes (4): AgentRole, Système de débat entre IA pour Betacryptobot Inspiré de Grokcloud : système de v, Enum, Grokcloud package for Betacryptobot - AI debate system components.

### Community 3 - "DebateAgent"
Cohesion: 0.33
Nodes (3): DebateAgent, Classe de base pour les agents du débat, Génère un argument basé sur le contexte et les arguments précédents

### Community 4 - ".conduct_debate"
Cohesion: 0.33
Nodes (5): DebateRound, example_usage(), Exemple d'utilisation du système de débat, Représente une ronde de débat, Conduit un débat sur un sujet donné          Args:             topic: Sujet du d

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DebateEngine` connect `DebateEngine` to `DebateArgument`, `debate_system.py`, `DebateAgent`, `.conduct_debate`?**
  _High betweenness centrality (0.433) - this node is a cross-community bridge._
- **Why does `DebateArgument` connect `DebateArgument` to `debate_system.py`, `DebateAgent`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Why does `DebateAgent` connect `DebateAgent` to `debate_system.py`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._