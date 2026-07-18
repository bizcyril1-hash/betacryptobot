"""
Système de débat entre IA pour Betacryptobot
Inspiré de Grokcloud : système de validation dual-IA pour réduire les biais d'analyse

Ce module implémente un système de débat entre un analyste, un contradicteur et un juge
pour évaluer les stratégies de trading et réduire les biais cognitifs.
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Chargement des variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentRole(Enum):
    ANALYSTE = "analyste"
    CONTREDICUTEUR = "contradicteur"
    JUGE = "juge"

@dataclass
class DebateArgument:
    """Représente un argument dans le débat"""
    agent_role: AgentRole
    content: str
    confidence: float  # 0.0 à 1.0
    timestamp: datetime
    evidence: List[str] = None

    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []

@dataclass
class DebateRound:
    """Représente une ronde de débat"""
    round_number: int
    arguments: List[DebateArgument]
    summary: str = ""
    consensus_reached: bool = False

class DebateAgent:
    """Classe de base pour les agents du débat"""

    def __init__(self, role: AgentRole, model_name: str = "default"):
        self.role = role
        self.model_name = model_name
        self.memory: List[DebateArgument] = []

    def generate_argument(self, context: str, previous_arguments: List[DebateArgument] = None) -> DebateArgument:
        """Génère un argument basé sur le contexte et les arguments précédents"""
        # Cette méthode serait implémentée avec un appel à un LLM réel
        # Pour l'instant, c'est une simulation

        if previous_arguments is None:
            previous_arguments = []

        # Simulation basique basée sur le rôle
        if self.role == AgentRole.ANALYSTE:
            content = f"Analyse initiale basée sur {context}: Tendance haussière détectée avec confiance modérée."
            confidence = 0.7
        elif self.role == AgentRole.CONTREDICUTEUR:
            content = f"Contre-argument : Les données présentées pourraient être biaisées par des événements récents. Recommandation de prudence."
            confidence = 0.6
        else:  # JUGE
            content = f"Synthèse : Après examen des arguments, la tendance semble modérément haussière mais nécessite confirmation."
            confidence = 0.75

        argument = DebateArgument(
            agent_role=self.role,
            content=content,
            confidence=confidence,
            timestamp=datetime.now(),
            evidence=[context] if context else []
        )

        self.memory.append(argument)
        return argument

class DebateEngine:
    """Moteur qui orchestre le débat entre les agents"""

    def __init__(self):
        self.analyste = DebateAgent(AgentRole.ANALYSTE, "analyst_model")
        self.contradicteur = DebateAgent(AgentRole.CONTREDICUTEUR, "critic_model")
        self.juge = DebateAgent(AgentRole.JUGE, "judge_model")
        self.rounds: List[DebateRound] = []

    def conduct_debate(self, topic: str, max_rounds: int = 3) -> Dict[str, Any]:
        """
        Conduit un débat sur un sujet donné

        Args:
            topic: Sujet du débat (ex: "Analyse de BTC pour les 24h prochaines")
            max_rounds: Nombre maximum de rounds de débat

        Returns:
            Dictionnaire contenant les résultats du débat
        """
        logger.info(f"Starting debate on topic: {topic}")

        previous_arguments = []

        for round_num in range(1, max_rounds + 1):
            logger.info(f"Starting round {round_num}")

            round_arguments = []

            # Tour de l'analyste
            analyst_arg = self.analyste.generate_argument(topic, previous_arguments)
            round_arguments.append(analyst_arg)

            # Tour du contradicteur
            critic_arg = self.contradicteur.generate_argument(topic, previous_arguments + [analyst_arg])
            round_arguments.append(critic_arg)

            # Tour du juge (synthèse)
            judge_arg = self.juge.generate_argument(topic, previous_arguments + [analyst_arg, critic_arg])
            round_arguments.append(judge_arg)

            # Créer la ronde
            debate_round = DebateRound(
                round_number=round_num,
                arguments=round_arguments,
                summary=self._generate_round_summary(round_arguments),
                consensus_reached=self._check_consensus(round_arguments)
            )

            self.roundsadernalized
        # Calculate the amount of trade to open
        #return round(amount_of_coin_to_buy, 8)
        return amount_of_coin_to_buy

    def _generate_round_summary(self, arguments: List[DebateArgument]) -> str:
        """Génère un résumé de la ronde"""
        analyst_arg = next((a for a in arguments if a.agent_role == AgentRole.ANALYSTE), None)
        critic_arg = next((a for a in arguments if a.agent_role == AgentRole.CONTREDICUTEUR), None)
        judge_arg = next((a for a in arguments if a.agent_role == AgentRole.JUGE), None)

        analyst_content = analyst_arg.content if analyst_arg else "Non disponible"
        critic_content = critic_arg.content if critic_arg else "Non disponible"
        judge_content = judge_arg.content if judge_arg else "Non disponible"

        summary = f"Analyste: {analyst_content[:50]}... | Contradicteur: {critic_content[:50]}... | Juge: {judge_content[:50]}..."
        return summary

    def _check_consensus(self, arguments: List[DebateArgument]) -> bool:
        """Vérifie si un consensus a été atteint"""
        # Logique simplifiée : si la confiance du juge est élevée et que les autres sont d'accord
        judge_arg = next((a for a in arguments if a.agent_role == AgentRole.JUGE), None)
        if not judge_arg:
            return False

        # Dans une implémentation réelle, on analyserait plus profondément les arguments
        return judge_arg.confidence > 0.8

    def _generate_final_decision(self) -> Dict[str, Any]:
        """Génère la décision finale basée sur tous les rounds"""
        if not self.rounds:
            return {"decision": "aucune_decision", "confidence": 0.0, "reasoning": "Aucun débat n'a eu lieu"}

        # Prendre la dernière décision du juge
        last_judge_arg = None
        for round_obj in reversed(self.rounds):
            for arg in round_obj.arguments:
                if arg.agent_role == AgentRole.JUGE:
                    last_judge_arg = arg
                    break
            if last_judge_arg:
                break

        if not last_judge_arg:
            return {"decision": "erreur", "confidence": 0.0, "reasoning": "Pas d'argument de juge trouvé"}

        # Déterminer la décision basée sur le contenu et la confiance
        content_lower = last_judge_arg.content.lower()
        if "haussier" in content_lower or "bullish" in content_lower or "acheter" in content_lower:
            decision = "acheter"
        elif "baissier" in content_lower or "bearish" in content_lower or "vendre" in content_lower:
            decision = "vendre"
        else:
            decision = "neutre"

        return {
            "decision": decision,
            "confidence": last_judge_arg.confidence,
            "reasoning": last_judge_arg.content,
            "evidence": list(set(last_judge_arg.evidence))  # Dédupliquer les preuves
        }

    def save_debate(self, debate_result: Dict[str, Any], filepath: str = None):
        """Sauvegarde le résultat du débat dans un fichier JSON"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"debate_{timestamp}.json"

        # Créer le répertoire si nécessaire
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(debate_result, f, indent=2, ensure_ascii=False, default=str)

        logger.info(f"Débat sauvegardé dans {filepath}")

    def load_debate(self, filepath: str) -> Dict[str, Any]:
        """Charge un débat précédemment sauvegardé"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)


def example_usage():
    """Exemple d'utilisation du système de débat"""
    engine = DebateEngine()

    # Exemple de sujet de débat
    topic = "Analyse du Bitcoin (BTC) pour les 24 prochaines heures basée sur les données récentes"

    # Conduire le débat
    result = engine.conduct_debate(topic, max_rounds=3)

    # Afficher les résultats
    print(f"Sujet du débat: {result['topic']}")
    print(f"Décision finale: {result['final_decision']['decision']} "
          f"(confiance: {result['final_decision']['confidence']:.2f})")
    print(f"Raisonnement: {result['final_decision']['reasoning']}")
    print(f"Nombre de rounds: {len(result.get('rounds', []))}")

    # Sauvegarder le débat
    #saver("saver")  # Assuming this was meant to be a method call
    #engine.save_debate(result, "debate_results/btc_analysis.json")

    return result

if __name__ == "__main__":
    # Exemple d'utilisation
    result = example_usage()
    print("\nRésultat complet du débat:")
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))