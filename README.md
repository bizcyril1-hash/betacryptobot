# Betacryptobot

Système de validation et d'optimisation des stratégies de trading crypto qui combine l'approche data-exogène de Promax avec le framework de validation dual-IA de GrockCloud.

## 🚀 Démarrage rapide

```bash
# 1. Cloner le dépôt
git clone <repository-url>
cd Betacryptobot

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# 5. Lancer une analyse de démarrage
python analyse_cryptobot.py --help
```

## 📁 Structure du projet

```
Betacryptobot/
├── .claude/              # Configuration Claude Code (skills, agents, hooks)
├── exogene/              # Collecteurs de données externes
│   ├── promax_*.py       # Inspiré de Promax
│   └── grockcloud_*.py   # Inspiré de GrockCloud
├── marche/               # Modules de trading et backtesting
│   ├── strategy_*.py     # Stratégies de trading
│   ├── backtest_*.py     # Modules de backtesting
│   └── execution_*.py    # Modules d'exécution
├── docs/                 # Documentation
├── tests/                # Tests unitaires
├── .env                  # Variables d'environnement (à créer)
├── requirements.txt      # Dépendances Python
├── CLAUDE.md             # Instructions pour Claude Code
└── README.md             # Ce fichier
```

## 🔗 Liens avec les projets associés

- **[Promax](https://github.com/votre-compte/promax)** : Focus sur la collecte de données exogènes (réseaux sociaux, attention publique) pour éclairer le risque crypto
- **[GrokCloud](https://github.com/votre-compte/grokcloud)** : Système de validation dual-IA pour les stratégies de trading (analyste, contradicteur, juge)

## 🛠️ Développement

Ce projet utilise la configuration Claude Code avancée avec :
- Skills spécialisés (agentdb, reasoningbank, sparc, swarm, v3-series, etc.)
- Agents personnalisés (browser, consensus, core, etc.)
- Hooks de sécurité et de productivité
- Workflows d'automatisation

Voir `.claude/` pour la configuration détaillée.

## 📄 Licence

MIT
