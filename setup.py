"""
Script d'installation pour le package pricer.

Ce `setup.py` définit le package à partir du sous-dossier `src` afin de
respecter la convention de packaging où le code source est
séparé du reste du dépôt.  Le back‑end (`pricer`) est
déclaré comme package principal.  Les modules hérités et le front‑end
ne sont pas installés par défaut car ils servent surtout à des fins
éducatives ou de démonstration.
"""

from setuptools import setup, find_packages

setup(
    name="pricer",
    version="0.1.0",
    author="Tom Louarn",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="Package de pricing d'instruments financiers (options, obligations, swaps)",
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        # matplotlib et tkinter restent optionnels pour le front
    ],
)