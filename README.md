# Pricer

Ce dépôt propose un **pricer complet** structuré de manière claire et modulaire.  Deux approches coexistent : un back‑end moderne sous forme de package Python (`pricer`) et un front‑end graphique basé sur Tkinter qui réutilise une API héritée.  La structure est pensée pour faciliter la compréhension du code et son évolution dans le temps.

## Contenu du projet

- **`src/back/pricer/`** : package objet contenant des classes pour pricer des options, obligations, swaps, des courbes de taux et un moteur de simulation Monte‑Carlo.  Chaque module est documenté et typé, ce qui permet une utilisation aisée dans vos propres scripts ou notebooks.

Le dossier `src/back` contient `pricer.py`, `equityOptionFunctions.py`, `currencyOptionFunctions.py`, `indexOptionFunctions.py`, `futuresOptionFunctions.py`, `bondsPricingFunctions.py`, etc.  

- **`src/front/`** : interface graphique Tkinter.  Le fichier `app.py` crée une fenêtre avec plusieurs onglets : calculateur d’options (Black–Scholes, volatilité implicite), simulateur Monte‑Carlo, calculateur d’obligations, swaps et gestion de la courbe de taux.  Les modules `window.py`, `tabs.py`, `label.py` et `widgets.py` encapsulent les composants graphiques.

- **Fichiers racine** :
  - `requirements.txt` : dépendances nécessaires (numpy, pandas, scipy, matplotlib, tkinter…).
  - `setup.py` : script d’installation pour créer un package Python à partir de `finance_pricer`.
  - `refonte_report.md` : rapport académique détaillant la refonte, les choix de conception et les justifications théoriques.
  - `README.md` (ce fichier) : guide de prise en main et de structure.

## Installation

1. Cloner le dépôt :

   ```bash
   git clone <repository_url>
   cd finance_pricer
   ```

2. Créer un environnement virtuel et installer les dépendances :

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Utilisation du front‑end Tkinter

L’interface graphique est basée sur Tkinter.  Pour la lancer :

```bash
cd src/front
python app.py
```

Une fenêtre s’ouvrira avec plusieurs onglets : vous pourrez pricer des options (avec calcul des greeks ou de la volatilité implicite), lancer des simulations Monte‑Carlo, évaluer une obligation et ses sensibilités, et valoriser un swap taux fixe/flottant.  L’interface repose encore sur l’API de `pricer.py` et des fonctions associées.

## Utilisation du back‑end

Vous pouvez également utiliser directement les classes du package `pricer` pour écrire vos propres scripts ou notebooks.  Par exemple, pour pricer une option européenne :

```python
from src.back.finance_pricer import EuropeanOption, OptionType

# Création d’une option européenne call
opt = EuropeanOption(
    spot=100,
    strike=105,
    maturity=0.5,
    volatility=0.25,
    rate=0.03,
    dividend_yield=0.0,
    option_type=OptionType.CALL,
)

results = opt.greeks()
print("Prix:", results["price"])  # prix
print("Delta:", results["delta"])  # delta
```

L’API moderne est entièrement documentée et typée.  Consultez le fichier `refonte_report.md` pour comprendre les décisions de conception et les principes théoriques sous‑jacents.
