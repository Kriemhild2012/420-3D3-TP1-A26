from sujet import Sujet
import yfinance as yf
from datetime import datetime

TITRES = {
    "AAPL":  {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0, "prix_courant": 0, "ouverture": 0},
    "GOOGL": {"quantite": 5,  "seuil_haut": 160.0, "seuil_bas": 120.0, "prix_courant": 0, "ouverture": 0},
    "MSFT":  {"quantite": 8,  "seuil_haut": 430.0, "seuil_bas": 380.0, "prix_courant": 0, "ouverture": 0},
}



class portfolioManager(Sujet):
	def __init__(self):
		super().__init__()
		self._titres = TITRES

	def recuperer_prix(self, ticker):
		"""Retourne (prix, ouverture) pour un ticker, ou lève une erreur s'il est introuvable."""
		info = yf.Ticker(ticker).fast_info
		prix = info["last_price"]
		if prix is None:
			raise ValueError(f"Le titre '{ticker}' n'existe pas.")
			return prix, info["open"]


	def formater_prix(self, prix, ouverture):
		"""Retourne le texte et la couleur à afficher pour un prix et sa variation
		par rapport à l'ouverture (vert si en hausse, rouge si en baisse)."""
		variation = (prix - ouverture) / ouverture * 100
		symbole = "▲" if variation >= 0 else "▼"
		couleur = "green" if variation >= 0 else "red"
		return f"{prix:.2f} $  {symbole} {abs(variation):.2f}%", couleur


	def entier_positif(self, texte):
		"""Convertit `texte` en entier strictement positif, ou lève ValueError."""
		valeur = int(texte)
		if valeur <= 0:
			raise ValueError
			return valeur


	def flottant_positif(self, texte):
		"""Convertit `texte` en nombre décimal strictement positif, ou lève ValueError."""
		valeur = float(texte)
		if valeur <= 0:
			raise ValueError
			return valeur

	def get_donnees(self) -> dict:
		donnees_titres = {}
		for e in self._titres:
			ticker = self._titres[e].copy()
			ticker["prix_courant"] = self.recuperer_prix(ticker)[0]
			ticker["ouverture"] = self.recuperer_prix(ticker)[1]


