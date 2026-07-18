# BTC-USDT — Export V5 inférences + market_context + prix

Généré le **2026-07-14** depuis MongoDB `cryptobot-db` (prod), symbole **BTC-USDT**.
Une ligne = **une inférence V5** (toutes les grilles `bar_shift_minutes`), enrichie du
`market_context` (join asof causal) et du prix (close + rendements forward).

## Fichiers
| Fichier | Lignes | Contenu |
|---|---|---|
| `btc_v5_inferences_marketcontext_price.csv[.gz]` | 99 670 | **Complet** — toutes les grilles bar_shift (0..14) |
| `btc_v5_shift0_only.csv[.gz]` | 12 464 | Série canonique 15 min uniquement (`bar_shift_minutes==0`) |

Couverture temporelle : inférences **2026-03-03 → 2026-07-14**. Le `market_context`
ne commence que le **2026-04-01** (avant : colonnes `mc_*` vides — c'est normal, la
collection n'existait pas). Prix issus des candles 1 min.

---

## Convention de temps (CRITIQUE — no-leak)
- `data_timestamp` = **début** de la barre 15 min d'entrée. **NE JAMAIS aligner dessus**
  (= look-ahead de 15 min).
- `inference_time` = `data_timestamp + 15 min` = **clôture de barre = moment de décision**.
  **Aligner tout backtest/analyse sur `inference_time`.** Actionnable ~1 min après
  (latence d'insertion médiane ~37 s).
- Les rendements forward (`ret_fwd_*`) et `close_at_inference` sont calculés **à partir de
  `inference_time`** (donc exécutables, sans fuite).
- `market_context` est joint en **asof backward** (dernier `mc_valid_time ≤ inference_time`) → causal.

## `bar_shift_minutes` (à lire avant d'utiliser le fichier complet)
Le pipeline écrit des inférences sur des grilles 15 min **décalées** (0, 2, 4, …, 14 min).
- `bar_shift_minutes == 0` = **série canonique**, modèles entraînés dessus. Utiliser
  `btc_v5_shift0_only.csv` pour une série 15 min propre.
- Les shifts **pairs** (2,4,…14) = updates intra-horaire (~toutes 2 min), **off-distribution**
  (modèles pas entraînés dessus) → utiles pour la fraîcheur live, à ne PAS mélanger naïvement
  avec le shift 0 en entraînement.
- Les shifts **impairs** (1,3,5…) sont quasi vides (~10 docs) = grilles mortes, à ignorer.

---

## Colonnes

### Sous-modèles V5 (le cœur)
La V5 = 3 perspectives indépendantes + 1 fusion. Régime 3-classes, ordre **toujours [FLAT, UP, DOWN]**.
Sémantique (horizon 1 barre = 15 min) :
- **directional** (`dir_*`) — « où » : y a-t-il un move qui vaut la peine (≥1.5 %/≥3 h) ? Horizon ~6 h.
- **trend_confirm** (`trend_*`) — « si » : tendance structurellement confirmée ? Veto lent. Horizon ~3 h.
- **exhaustion** (`exh_*`) — « quand » : momentum frais ou épuisé ? Filtre de timing. Horizon ~8 h.
- **fusion_simple** (`fus_*`) — méta-consensus orienté ground-truth « directional ». **Signal de décision recommandé.**

| Colonne | Sens |
|---|---|
| `dir_flat/up/down`, `dir_label` | probas + argmax de directional |
| `trend_flat/up/down`, `trend_label` | idem trend_confirm |
| `exh_flat/up/down`, `exh_label` | idem exhaustion |
| `fus_flat/up/down`, `fus_label`, `fus_argmax` | idem fusion_simple |
| `fus_max_proba` | max des 3 probas (confiance brute) |
| `fus_entropy_score` | ∈[0,1], **1 = certain** (gating recommandé) |
| `fus_directional_spread` | \|p_up − p_down\| = conviction directionnelle hors FLAT |
| **dérivés** `dir_net`, `trend_net`, `exh_net`, `fus_net` | `p_up − p_down` (signal signé ∈[−1,1]) |
| **dérivé** `fus_conf` | `1 − p_flat` (conviction = pas-flat) |

**Gating recommandé** (jamais dans les modèles eux-mêmes, à notre charge) : ne trader que si
`fus_entropy_score` haut ET `fus_directional_spread` haut ; label=FLAT ou faible confiance = rester dehors.

### market_context (`mc_*`) — 91 champs, join asof
Contexte marché calculé à `mc_valid_time`. Sélection notable :
- `mc_regime_dir` (BULL/BEAR/…), `mc_dir.consensus_score` (dir consensus cross-asset ∈[−1,1]),
  `mc_dir.strength`, `mc_dir.consensus_z`, `mc_dir.entropy_score`, `mc_trend_dir_score`.
- Vol : `mc_vol.realized_vol_1h/4h/24h`, `mc_vol.atr_pct`, `mc_vol.vol_of_vol`, `mc_vol.pctile_*`.
- Flow : `mc_flow.adx_14`, `mc_flow.oi_z_1d`, `mc_flow.delta_z_1d`. Funding : `mc_funding.z_7d`.
- Risque : `mc_risk.drawdown_24h_pct`, `mc_risk.runup_24h_pct`.
- Marché global : `mc_market.breadth`, `mc_market.conviction`, `mc_market.risk_score`,
  `mc_market.avg_pairwise_corr`, `mc_market.btc_leadership`, `mc_market.dispersion`.
- Session : `mc_session.active_session`, `mc_session.minutes_to_funding`.
- Divergence/relatif : `mc_divergence_flag`, `mc_asset_vs_consensus`, `mc_corr_to_consensus`,
  `mc_beta_to_btc` (pour BTC = 1.0 par construction).

### Prix (candles 1 min)
| Colonne | Sens |
|---|---|
| `close_at_inference` | close 1 min à `inference_time` |
| `ret_fwd_15m/1h/4h/24h` | rendement forward `close(t+H)/close(t) − 1` (exécutable, no-leak) |

---

## Notes de qualité
- `dir_net`/`fus_net` : ~0.1 % de NaN (docs sans perspectives). `ret_fwd_24h` : ~2 % NaN en fin de série.
- `mc_*` : 100 % NaN avant 2026-04-01 (attendu), 0.3 % après.
- Corrélation brute `dir_net` ↔ `ret_fwd_4h` ≈ **+0.03** (shift0) — signal faible, à traiter avec rigueur
  (déflater le multiple-testing, IS/OOS, coûts ~8 bps aller-retour). Le prix reste dur à battre net-de-coûts.

Toute question sur la génération/schéma → Romain.
