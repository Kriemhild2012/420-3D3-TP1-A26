from modeles.sujet import Sujet
import yfinance as yf


class PortfolioManager(Sujet):
    def __init__(self):
        super().__init__()
        self._titres = {
            "AAPL": {
                "quantite": 10,
                "seuil_haut": 200.0,
                "seuil_bas": 150.0,
                "prix_courant": None,
                "ouverture": None,
            },
            "GOOGL": {
                "quantite": 5,
                "seuil_haut": 160.0,
                "seuil_bas": 120.0,
                "prix_courant": None,
                "ouverture": None,
            },
            "MSFT":  {
                "quantite": 8,
                "seuil_haut": 430.0,
                "seuil_bas": 380.0,
                "prix_courant": None,
				"ouverture": None,
            }
        }

    def recuperer_prix(self, ticker):
        info = yf.Ticker(ticker).fast_info
        prix = info["last_price"]
        ouverture = info["open"]

        if prix is None:
            raise ValueError(f"Le titre '{ticker}' n'existe pas.")

        return prix, ouverture

    def rafraichir_prix(self):
        for ticker, infos in self._titres.items():
            prix, ouverture = self.recuperer_prix(ticker)
            infos["prix_courant"] = prix
            infos["ouverture"] = ouverture

        self.notifier()

    def ajouter_titre(self, ticker, quantite, seuil_bas, seuil_haut):
        if ticker in self._titres:
            raise ValueError("Ce titre existe déjà.")

        prix, ouverture = self.recuperer_prix(ticker)

        self._titres[ticker] = {
            "quantite": quantite,
            "seuil_haut": seuil_haut,
            "seuil_bas": seuil_bas,
            "prix_courant": prix,
            "ouverture": ouverture,
        }

        self.notifier()

    def retirer_titre(self, ticker):
        if ticker not in self._titres:
            raise ValueError("Ce titre n'existe pas.")

        del self._titres[ticker]
        self.notifier()

    def modifier_titre(self, ticker, quantite=None,
                       seuil_bas=None, seuil_haut=None):
        if ticker not in self._titres:
            raise ValueError("Ce titre n'existe pas.")

        infos = self._titres[ticker]

        if quantite is not None:
            infos["quantite"] = quantite
        if seuil_bas is not None:
            infos["seuil_bas"] = seuil_bas
        if seuil_haut is not None:
            infos["seuil_haut"] = seuil_haut

        self.notifier()

    def get_donnees(self):
        return {
            "titres": {
                ticker: infos.copy()
                for ticker, infos in self._titres.items()
            },
            "valeur_totale": sum(
                infos["prix_courant"] * infos["quantite"]
                for infos in self._titres.values()
                if infos["prix_courant"] is not None
            ),
        }