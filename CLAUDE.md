# CLAUDE.md — Instructions permanentes du projet Betacryptobot
(Lu automatiquement par Claude Code à chaque session. Ne pas renommer.)

## Profil de l'utilisateur
- Débutant complet en programmation. TOUJOURS expliquer chaque action en une phrase
  simple, en français, AVANT de l'exécuter. Jamais de jargon sans définition.
- Souhaite un maximum d'autonomie de Claude Code : proposer et enchaîner les étapes
  sans attendre qu'on les demande, en validant seulement les points clés.

## Objectif du projet
**Betacryptobot** — Système d'analyse et de trading de cryptomonnaies qui combine
les forces de deux approches établies :
1. **Promax** : Focus sur l'analyse de l'exogénéité (sentiment social, attention publique) 
   pour éclairer le risque crypto (pas la direction des prix)
2. **Grokcloud** : Système de débat entre deux IA pour réduire les biais d'analyse

## Architecture conceptuelle
```
                    +------------------+
                    |   Betacryptobot  |
                    +--------+---------+
                             |
        +--------------------+--------------------+
        |                                         |
+-------v-------+                       +---------v----------+
|   Module      |                       |   Module           |
|   Promax-Style|                       |   Grokcloud-Style  |
|   (Exogenous) |                       |   (Debate System)  |
+-------+-------+                       +---------+----------+
        |                                         |
        |                                         |
+-------v-------+                       +---------v----------+
|   Data        |                       |   LLM Debate       |
|   Collection  |                       |   System           |
+-------+-------+                       +---------+----------+
        |                                         |
        |                                         |
+-------v-------+                       +---------v----------+
|   Storage     |                       |   Decision         |
|   & Cache     |                       |   Engine           |
+-------+-------+                       +---------+----------+
        \                                         /
         \                                       /
          \                                     /
           \                                     /
            \                                   /
             \                                 /
              \                               /
               \                             /
                \                           /
                 \                         /
                  \                       /
                   \                     /
                    \                   /
                     \                 /
                      \               /
                       \             /
                        \           /
                         \         /
                          \       /
                           \     /
                            \   /
                             \ /
                     +-------v-------+
                     |   Action      |
                     |   Engine      |
                     |   (Trading/   |
                     |   Alerting)   |
                     +---------------+
```

## Pipeline de décision
1. **Collecte de données** (style Promax) :
   - Données de marché (prix, volume, order book)
   - Données on-chain (flux, actifs détenus)
   - Données sociales (Reddit, Twitter, forums)
   - Données macro (indicateurs économiques, taux d'intérêt)
   - Données alternatives (Google Trends, Wikipedia views, événements GDELT)

2. **Prétraitement & caractéristiques** :
   - Nettoyage et normalisation des données
   - Création de caractéristiques techniques (indicateurs, patterns)
   - Création de caractéristiques sentimentales (NLP sur texte)
   - Création de caractéristiques macroéconomiques
   - Création de facteurs d'exogénéité (mesure de l'attention extérieure)

3. **Analyse multi-agents** (style Grokcloud) :
   - Agent Analyste : Interprète les données et suggère une action
   - Agent Contredicteur : Identifie les failles dans l'analyse
   - Agent Juge : Évalue les deux arguments et rend une décision
   - Plusieurs rounds de débat possibles pour affiner l'analyse

4. **Gestion du risque** :
   - Évaluation de la taille de position basée sur la volatilité
   - Calcul du Value-at-Risk (VaR) et du Expected Shortfall (ES)
   - Gestion de la diversification entre actifs
   - Stop-loss et take-profit dynamiques

5. **Exécution** :
   - Génération d'ordres de marché ou limites
   - Soumission aux exchanges via CCXT
   - Suivi en temps réel des positions
   - Reporting et alertes

## Règles de fonctionnement
- **Pas de conseil en investissement** : Le système fournit des signaux à
  backtester et valider, pas des recommandations d'achat/vente directes
- **Backtesting obligatoire** : Toute stratégie doit être rigoureusement
  testée sur des données historiques avant déploiement
- **Gestion du risque prioritaire** : La préservation du capital passe
  toujours avant la recherche de rendement
- **Transparence** : Toutes les décisions doivent être explicables et
  traçables jusqu'aux données sources
- **Sécurité avant tout** : Jamais d'exposition aux clés API ou aux fonds
  réels sans validation approfondie

## Phases de développement
1. **Phase 0** : Infrastructure de collecte de données (inspiré de Promax)
2. **Phase 1** : Système de débat entre IA (inspiré de Grokcloud)
3. **Phase 2** : Intégration et génération de signaux
4. **Phase 3** : Gestion du risque et exécution
5. **Phase 4** : Optimisation et mise en production

## Rôles des IA dans ce système
- **Analyste Principal** : Modèle puissant pour l'analyse initiale des données
- **Contradicteur** : Modèle différent qui challenge l'analyse initiale
- **Juge** : Troisième modèle (ou même que l'un des précédents) qui synthétise
  et donne la décision finale
- **Spécialistes de domaine** : Experts en analyse technique, fondamentale, 
 
  ou sentimentale selon les besoins
