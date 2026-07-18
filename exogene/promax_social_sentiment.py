"""
Module de collecte de données exogènes pour Betacryptobot
Inspiré de Promax : collecte de sentiment sur les réseaux sociaux et d'attention publique

Ce module collecte des données depuis Reddit et Twitter, effectue une analyse de sentiment,
et stocke les résultats pour une utilisation ultérieure dans l'analyse de risque crypto.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time

import praw  # Reddit API
import tweepy  # Twitter API
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import duckdb  # DuckDB for storage

# Chargement des variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialSentimentCollector:
    def __init__(self):
        """Initialise le collecteur avec les API disponibles."""
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        # Initialisation de Reddit (si les credentials sont disponibles)
        self.reddit = None
        try:
            self.reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                user_agent=os.getenv("REDDIT_USER_AGENT", "betacryptobot:0.1 (by u/your_username)")
            )
            # Test de connexion
            self.reddit.user.me()
            logger.info("Connexion à Reddit établie")
        except Exception as e:
            logger.warning(f"Impossible de se connecter à Reddit : {e}")
            self.reddit = None

        # Initialisation de Twitter/X (si les credentials sont disponibles)
        self.twitter_client = None
        try:
            self.twitter_client = tweepy.Client(
                bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
                consumer_key=os.getenv("TWITTER_API_KEY"),
                consumer_secret=os.getenv("TWITTER_API_SECRET"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                wait_on_rate_limit=True
            )
            # Test de connexion
            self.twitter_client.get_me()
            logger.info("Connexion à Twitter établie")
        except Exception as e:
            logger.warning(f"Impossible de se connecter à Twitter : {e}")
            self.twitter_client = None

        # Initialisation de la base de données DuckDB
        self.db_path = "data/social_sentiment.duckdb"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = duckdb.connect(self.db_path)
        self._create_tables()

    def _create_tables(self):
        """Crée les tables nécessaires si elles n'existent pas."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS redemptions (
                id VARCHAR PRIMARY KEY,
                platform VARCHAR,
                created_at TIMESTAMP,
                collected_at TIMESTAMP,
                raw_data JSON,
                sentiment_score DOUBLE,
                sentiment_label VARCHAR,
                text TEXT
            )
        """)
        logger.info("Tables de base de données vérifiées/créées")

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyse le sentiment d'un texte et retourne le score et l'étiquette."""
        scores = self.sentiment_analyzer.polarity_scores(text)
        # La méthode de VADER retourne un dictionnaire avec 'neg', 'neu', 'pos', 'compound'
        # Nous utilisons le score compound pour une mesure globale de sentiment
        compound = scores['compound']
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        return {
            "score": compound,
            "label": label,
            "details": scores
        }

    def collect_reddit_posts(self, subreddits: List[str] = None, limit: int = 100) -> List[Dict]:
        """
        Collecte des posts depuis les subreddits spécifiés.

        Args:
            subreddits: Liste des subreddits à surveiller (défaut: courants crypto)
            limit: Nombre maximal de posts à récupérer par subreddit

        Returns:
            Liste de dictionnaires contenant les données des posts
        """
        if not self.reddit:
            logger.error("Reddit client non initialisé. Vérifiez les credentials.")
            return []

        if subreddits is None:
            subreddits = ["CryptoCurrency", "Bitcoin", "ethtrader", "binance", "CryptoMarkets"]

        collected_posts = []

        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                # Récupérer les posts les plus récents
                for post in subreddit.new(limit=limit):
                    # Éviter les posts déjà collectés (basé sur l'ID)
                    # Nous pourrions vérifier en base, mais pour simplicité, on collecte tout et on déduplique plus tard
                    text = f"{post.title} {post.selftext}"
                    sentiment = self._analyze_sentiment(text)

                    post_data = {
                        "id": f"reddit_{post.id}",
                        "platform": "reddit",
                        "created_at": datetime.fromtimestamp(post.created_utc),
                        "collected_at": datetime.now(),
                        "raw_data": json.dumps({
                            "title": post.title,
                            "selftext": post.selftext,
                            "score": post.score,
                            "num_comments": post.num_comments,
                            "upvote_ratio": post.upvote_ratio,
                            "subreddit": subreddit_name,
                            "url": post.url
                        }),
                        "sentiment_score": sentiment["score"],
                        "sentiment_label": sentiment["label"],
                        "text": text[:500]  # Limiter la taille du texte stocké
                    }
                    collected_posts.append(post_data)

                logger.info(f"Collecté {limit} posts depuis r/{subreddit_name}")
                # Respecter les limites de taux de Reddit (attendre un peu entre les subreddits)
                time.sleep(1)

            except Exception as e:
                logger.error(f"Erreur lors de la collecte depuis r/{subreddit_name}: {e}")

        return collected_posts

    def collect_twitter_tweets(self, query: str = "(bitcoin OR btc OR ethereum OR eth) lang:en -is:retweet",
                               max_results: int = 100) -> List[Dict]:
        """
        Collecte des tweets depuis Twitter/X correspondant à une requête.

        Args:
            query: Requête de recherche Twitter (défaut: termes crypto en anglais, pas de retweets)
            max_results: Nombre maximal de tweets à récupérer (max 100 par requête)

        Returns:
            Liste de dictionnaires contenant les données des tweets
        """
        if not self.twitter_client:
            logger.error("Twitter client non initialisé. Vérifiez les credentials.")
            return []

        collected_tweets = []

        try:
            # Recherche récente des tweets
            tweets = self.twitter_client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "lang", "author_id"],
                expansions=["author_id"]
            )

            if not tweets.data:
                logger.info("Aucun tweet trouvé pour la requête")
                return []

            # Créer un dictionnaire des utilisateurs pour inclure les infos d'utilisateur si nécessaire
            users = {u["id"]: u for u in tweets.includes.get("users", [])} if tweets.includes else {}

            for tweet in tweets.data:
                text = tweet.text
                sentiment = self._analyze_sentiment(text)

                # Métriques publiques
                metrics = tweet.public_metrics if hasattr(tweet, 'public_metrics') else {}

                tweet_data = {
                    "id": f"twitter_{tweet.id}",
                    "platform": "twitter",
                    "created_at": tweet.created_at,
                    "collected_at": datetime.now(),
                    "raw_data": json.dumps({
                        "text": tweet.text,
                        "author_id": tweet.author_id,
                        "metrics": metrics,
                        "language": tweet.lang,
                        "query": query
                    }),
                    "sentiment_score": sentiment["score"],
                    "sentiment_label": sentiment["label"],
                    "text": text[:500]  # Limiter la taille du texte stocké
                }
                collected_tweets.append(tweet_data)

            logger.info(f"Collecté {len(collected_tweets)} tweets pour la requête: {query}")

        except Exception as e:
            logger.error(f"Erreur lors de la collecte des tweets: {e}")

        return collected_tweets

    def store_data(self, data_list: List[Dict]):
        """
        Stocke une liste de données de posts/tweets dans la base de données DuckDB.

        Args:
            data_list: Liste de dictionnaires contenant les données à stocker
        """
        if not data_list:
            logger.warning("Aucune donnée à stocker")
            return

        # Préparer les données pour l'insertion
        rows = []
        for data in data_list:
            rows.append((
                data["id"],
                data["platform"],
                data["created_at"],
                data["collected_at"],
                data["raw_data"],
                data["sentiment_score"],
                data["sentiment_label"],
                data["text"]
            ))

        # Insérer ou mettre à jour (en cas de doublon sur l'ID)
        self.conn.executemany("""
            INSERT OR REPLACE INTO redemptions
            (id, platform, created_at, collected_at, raw_data, sentiment_score, sentiment_label, text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)

        logger.info(f"Stocké {len(data_list)} enregistrements en base de données")

    def run_collection_cycle(self, reddit_limit: int = 50, twitter_max_results: int = 50):
        """
        Exécute un cycle complet de collecte : Reddit puis Twitter.

        Args:
            reddit_limit: Nombre de posts à récupérer par subreddit Reddit
            twitter_max_results: Nombre de tweets à récupérer par requête
        """
        logger.info("Début du cycle de collecte des données sociales")

        # Collecte depuis Reddit
        reddit_data = self.collect_reddit_posts(limit=reddit_limit)
        if reddit_data:
            self.store_data(reddit_data)

        # Collecte depuis Twitter
        twitter_data = self.collect_twitter_tweets(max_results=twitter_max_results)
        if twitter_data:
            self.store_data(twitter_data)

        logger.info("Fin du cycle de collecte des données sociales")

if __name__ == "__main__":
    # Exemple d'utilisation directe du module
    collector = SocialSentimentCollector()
    collector.run_collection_cycle()

    # Afficher un aperçu des données collectées
    result = collector.conn.execute("SELECT COUNT(*) as count, platform, sentiment_label FROM redemptions GROUP BY platform, sentiment_label").fetchdf()
    print("Aperçu des données collectées :")
    print(result)