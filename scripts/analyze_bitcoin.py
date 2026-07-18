#!/usr/bin/env python3
"""
Script d'analyse de données Bitcoin utilisant un modèle répétable.
Version : 0.2
"""

import csv
import sys
import os
from datetime import datetime
from pathlib import Path

def load_bitcoin_data(file_path):
    """
    Charge les donnees Bitcoin depuis un fichier CSV.
    Le fichier doit avoir les colonnes : timestamp, open, high, low, close, volume
    """
    data = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convertir les valeurs numeriques
                row['open'] = float(row['open'])
                row['high'] = float(row['high'])
                row['low'] = float(row['low'])
                row['close'] = float(row['close'])
                row['volume'] = float(row['volume'])
                data.append(row)
        print(f"[OK] Donnees chargees : {len(data)} enregistrements depuis {file_path}")
        return data
    except FileNotFoundError:
        print(f"[ERREUR] Fichier {file_path} introuvable.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERREUR] Erreur lors du chargement des donnees : {e}")
        sys.exit(1)

def calculate_simple_moving_average(data, window, price_field='close'):
    """Calcule la moyenne mobile simple sur une fenêtre donnée."""
    if len(data) < window:
        return None
    prices = [item[price_field] for item in data]
    sma = []
    for i in range(len(prices)):
        if i < window - 1:
            sma.append(None)
        else:
            window_data = prices[i - window + 1:i + 1]
            sma.append(sum(window_data) / window)
    return sma

def calculate_volatility(data, window=10):
    """Calcule la volatilité (écart-type des rendements) sur une fenêtre donnée."""
    if len(data) < window + 1:
        return None
    closes = [item['close'] for item in data]
    returns = []
    for i in range(1, len(closes)):
        returns.append((closes[i] - closes[i-1]) / closes[i-1])

    volatility = []
    for i in range(len(returns)):
        if i < window - 1:
            volatility.append(None)
        else:
            window_data = returns[i - window + 1:i + 1]
            mean = sum(window_data) / window
            variance = sum((x - mean) ** 2 for x in window_data) / window
            volatility.append(variance ** 0.5)
    return volatility

def generate_analysis_report(data, template_path, output_path):
    """
    Génère un rapport d'analyse en remplissant le modèle avec les résultats.
    """
    # Lire le modèle
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
    except FileNotFoundError:
        print(f"✗ Erreur : Modèle {template_path} introuvable.")
        sys.exit(1)

    # Calculer quelques indicateurs de base
    closes = [item['close'] for item in data]
    current_price = closes[-1] if closes else 0
    price_change_24h = ((closes[-1] - closes[-2]) / closes[-2]) * 100 if len(closes) >= 2 else 0

    # Moyennes mobiles simples
    sma_7 = calculate_simple_moving_average(data, 7)
    sma_30 = calculate_simple_moving_average(data, 30)
    current_sma_7 = sma_7[-1] if sma_7 and sma_7[-1] is not None else 0
    current_sma_30 = sma_30[-1] if sma_30 and sma_30[-1] is not None else 0

    # Volatilité
    volatility = calculate_volatility(data, 10)
    current_volatility = volatility[-1] if volatility and volatility[-1] is not None else 0

    # Remplacer les placeholders dans le modèle
    filled_template = template.replace('{date}', datetime.now().strftime('%Y-%m-%d'))

    # Nous allons ajouter une section de résultats après l'en-tête
    # Pour simplifier, nous allons insérer un résumé après la ligne de titre
    lines = filled_template.split('\n')
    # Insérer après la deuxième ligne (après le titre et la ligne vide)
    insert_index = 2
    results_section = [
        "",
        "## Résumé des Données Analysées",
        f"- Prix actuel : ${current_price:,.2f}",
        f"- Variation 24h : {price_change_24h:+.2f}%",
        f"- Moyenne mobile 7 jours : ${current_sma_7:,.2f}",
        f"- Moyenne mobile 30 jours : ${current_sma_30:,.2f}",
        f"- Volatilité (10 jours) : {current_volatility:.2%}",
        "",
        "---",
        ""
    ]
    lines[insert_index:insert_index] = results_section
    filled_template = '\n'.join(lines)

    # Écrire le rapport de sortie
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(filled_template)
        print(f"[OK] Rapport genere : {output_path}")
    except Exception as e:
        print(f"[ERREUR] Erreur lors de l'ecriture du rapport : {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_bitcoin.py <chemin_vers_fichier_csv> [chemin_vers_modele] [chemin_vers_sortie]")
        print("Exemple: python analyze_bitcoin.py data/bitcoin.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    template_path = sys.argv[2] if len(sys.argv) > 2 else "analysis_templates/bitcoin_analysis_template_v0.2.md"
    output_path = sys.argv[3] if len(sys.argv) > 3 else f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    # Utiliser le repertoire de travail courant comme base
    base_dir = Path.cwd()
    csv_path = base_dir / csv_path if not Path(csv_path).is_absolute() else Path(csv_path)
    template_path = base_dir / template_path if not Path(template_path).is_absolute() else Path(template_path)
    output_path = base_dir / output_path if not Path(output_path).is_absolute() else Path(output_path)

    print("Debut de l'analyse des donnees Bitcoin...")
    print(f"Fichier de donnees : {csv_path}")
    print(f"Modele utilise : {template_path}")
    print(f"Sortie du rapport : {output_path}")
    print("-" * 50)

    # Charger les donnees
    data = load_bitcoin_data(csv_path)

    # Generer le rapport
    generate_analysis_report(data, template_path, output_path)

    print("-" * 50)
    print("Analyse terminee !")
    print(f"Consultez le rapport : {output_path}")

if __name__ == "__main__":
    main()