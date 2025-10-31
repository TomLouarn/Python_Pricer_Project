# Justification des choix de conception

L’objectif est double : fournir des outils de pricing
fiables pour un desk delta one ou volatilité, et démontrer une
capacité à appliquer des principes d’ingénierie logicielle.

## 1. Structuration en package

Le projet est organisé comme un package Python installable
`pricer` (cf. arborescence ci‑dessous). Cette structuration
répond à plusieurs objectifs :

1. **Isolation et réutilisabilité** : chaque module (options, obligations, swaps,
   courbes, Monte Carlo) est autonome et peut être importé séparément.
2. **Testabilité** : un package facilite l’écriture de tests unitaires
   ciblant chaque classe ou fonction sans dépendre de l’interface
   graphique.
3. **Distribution** : l’ajout ultérieur d’un `setup.py` ou d’un
   `pyproject.toml` permettra de publier le package sur PyPI ou de
   l’installer via `pip`.

Arborescence simplifiée :

```
pricer/
├── __init__.py
├── options.py        # Options européennes, américaines, asiatiques, barrières
├── bonds.py          # Obligations à taux fixe
├── swaps.py          # Swaps de taux et DV01
├── rates.py          # Courbe de taux zéro (interpolation, discounting)
└── monte_carlo.py    # Générateur Monte Carlo générique
refonte_report.md     # présent document
```

## 2. Utilisation de `dataclasses` et `Enum`

Les instruments financiers sont représentés par des classes décorées
`@dataclass`. Cela génère automatiquement les méthodes d’initialisation
et simplifie l’écriture tout en imposant des types clairs pour chaque
attribut. Par exemple, `EuropeanOption` hérite d’une classe de base
`BaseOption` qui regroupe les paramètres communs (spot, strike,
maturité, volatilité, taux, dividende, type d’option). Ce design
présente plusieurs avantages :

* **Lisibilité** : les arguments sont nommés, ce qui supprime les
  ambiguïtés des listes positionnelles.
* **Validation** : la méthode `__post_init__` vérifie les valeurs
  (volatilité et maturité positives), améliorant la robustesse.
* **Extensibilité** : des méthodes `price()` et `greeks()` peuvent être
  redéfinies dans les sous‑classes (américaines, asiatiques,
  barrières), tandis que des méthodes communes (calcul de `d1`, `d2`)
  restent partagées.

L’énumération `OptionType` formalise les deux types de payoff (call,
put), évitant les chaînes de caractères magiques.

## 3. Factorisation du modèle Black–Scholes

Dans l’implémentation d’origine, quatre modules différents
(
`equityOptionFunctions.py`, `currencyOptionFunctions.py`,
`indexOptionFunctions.py`, `futuresOptionFunctions.py`
) recopiaient les mêmes formules en changeant simplement la variable
« dividende ».  La nouvelle classe `EuropeanOption` accepte un
paramètre `dividend_yield`. Selon sa valeur (0 % pour un future,
taux de dividende pour un indice, taux étranger pour une option sur
devises), la formule reste unique. Cette factorisation réduit les
duplications, facilite la maintenance et démontre une compréhension
académique du modèle : dans Black–Scholes, le dividende continu
amende le terme de dérive de la même façon qu’un taux étranger.

Les sensitiviés (delta, gamma, vega, theta, rho) sont calculées selon
les dérivées analytiques de Black–Scholes, avec un ajustement sur
l’actualisation (`disc_r`, `disc_q`). Cette implémentation est plus
compacte et modulaire que dans le code original.

## 4. Arbre binomial vectorisé pour les options américaines

Pour les options américaines, l’algorithme de Cox–Ross–Rubinstein est
reformulé dans la classe `AmericanOption`. L’utilisation de `numpy`
permet de vectoriser le calcul des valeurs terminales et d’éviter les
boucles imbriquées. En outre, les greeks sont obtenus via des
différences finies, méthode académique lorsqu’il n’existe pas de
formule fermée. Un paramètre `steps` offre à l’utilisateur un
contrôle granulaire sur la précision/complexité.

## 5. Options exotiques (asiatiques, barrière)

Les classes `AsianOption` et `BarrierOption` illustrent l’extension
possible à des payoffs exotiques :

- L’option asiatique utilise un simulateur Monte Carlo interne.
  L’approche consiste à générer `n_simulations` trajectoires du
  sous‑jacent selon un mouvement brownien géométrique, puis à
  calculer la moyenne arithmétique des prix pour déterminer le payoff.
  Les greeks sont évalués par différences finies, solution classique
  lorsque les formules analytiques sont complexes.
- L’option barrière « up‑and‑out » reprend l’idée de la technique de
  rééchantillonnage (« stretch technique »). La barrière est
  incorporée directement dans la rétro‑propagation sur un arbre
  trinomial. L’implémentation est généralisable à d’autres types de
  barrières en changeant la condition d’extinction.

## 6. Obligations et swaps

La classe `FixedRateBond` encapsule le calcul du prix, de la durée,
de la convexité et du DV01 d’une obligation :

1. **Calendrier des flux** : la méthode `_payment_schedule()` génère
   automatiquement les dates de paiements en fonction de la fréquence et
   ajuste au jour ouvré suivant. Elle calcule la part du coupon à chaque
   période et ajoute le principal à l’échéance.
2. **Actualisation** : l’utilisation d’une `ZeroCurve` externalise
   l’interpolation des taux et clarifie les responsabilités.
3. **YTM et sensibilités** : le taux de rendement actuariel est
   déterminé via `numpy_financial.irr`, et la DV01 est obtenue en
   recalculant le prix après un shift de 1 bp sur la courbe.

Pour les swaps, la classe `InterestRateSwap` génère les deux jambes à
partir des fréquences et des bases de calcul. Le prix est la somme des
flux actualisés (positifs pour la jambe fixe, négatifs pour la
flottante). La DV01 est calculée en évaluant le swap avec une courbe
shiftée.  Les forward rates de la jambe flottante sont extraits de la
courbe via `ZeroCurve.forward_rate()` ; ils correspondent aux taux
prévisibles à la date de fixation du flux.

## 7. Courbe de taux (`ZeroCurve`)

La classe `ZeroCurve` centralise l’interpolation des taux (via
`scipy.interpolate.interp1d`), le calcul du facteur d’actualisation et
le bump de la courbe. Elle prend en entrée un DataFrame indexé par des
dates et produisant des taux en %. Les méthodes :

- `forward_rate(date)` : renvoie le taux au format décimal à une date
  donnée (interpolation si besoin).
- `discount_factor(date)` : calcule exp(−r × t) où t est le temps en
  années entre la première date de la courbe et la date cible.
- `bump(bp)` : retourne une nouvelle courbe décalée de `bp` (en
  pourcentage).

Cette abstraction simplifie la gestion des taux sans risque et rend
l’algorithme indépendant de la provenance de la courbe (Excel,
base de données, API).

## 8. Simulation Monte Carlo

Le module `monte_carlo.py` propose la classe `MonteCarloEngine`
capable de générer des trajectoires log‑normales ou de Merton. Les
paramètres du modèle de sauts (intensité, moyenne, volatilité)
peuvent être spécifiés. La méthode `price_european()` renvoie le prix
d’une option européenne ainsi que l’erreur standard de la simulation.
Cette classe peut servir à valider les résultats obtenus par
Black–Scholes ou à simuler des stratégies de couverture plus
complexes.

## 9. Explications académiques des choix

1. **Abstraction et modularité :** en décomposant les instruments
   financiers en classes, on respecte le principe de responsabilité
   unique (Single Responsibility Principle) et on facilite l’extension
   future (ex. ajout d’options lookback, de swaps amortissants).
2. **Vectorisation et performance :** l’utilisation de `numpy` dans
   l’arbre binomial ou Monte Carlo évite des boucles explicites et
   exploite la rapidité des opérations sur tableaux. Ce choix est
   essentiel pour des simulations intensives, comme c’est le cas en
   trading quantitatif.
3. **Systématisation des greeks :** un portefeuille de trading doit
   connaître ses sensibilités.  L’implémentation analytique des greeks
   (lorsqu’elle existe) est privilégiée pour sa précision.  Sinon,
   l’approximation par différences finies est commentée et paramétrée.
4. **Gestion des taux divergents (dividende/étranger)** : en
   considérant le dividende continu comme un ajustement de la dérive,
   on uniformise les formules Black–Scholes pour les actions, indices,
   devises et futures. Cette vision est standard dans la littérature et
   évite la duplication.
5. **Interfaçage utilisateur séparé** : le code de calcul est
   entièrement découplé de l’interface graphique. Ceci permet de
   construire une UI (Tkinter, Streamlit, etc.) qui appelle simplement
   les classes du package, tout en facilitant les tests automatiques.

## 10. Prochaines étapes

Cette refonte offre une base solide mais perfectible :

- Ajouter des tests unitaires (via `pytest`) pour valider chaque
  instrument et garantir l’exactitude des formules.
- Étendre les classes d’options exotiques pour couvrir toutes les
  barrières et proposer un calcul explicite du theta et du rho.
- Intégrer des calendriers de jours ouvrés (ex. calendrier TARGET2
  via `pandas_market_calendars`) afin de gérer correctement les jours
  fériés.
- Mettre en place un packaging complet (`setup.py` ou
  `pyproject.toml`) et rédiger un README.md avec des exemples
  d’utilisation pour chaque module.
- Réaliser un front‑end moderne (ex. Streamlit) utilisant ce
  package, illustrant votre maîtrise des stacks back/front.
  
