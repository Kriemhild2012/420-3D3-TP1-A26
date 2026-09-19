from modeles.sujet import Sujet
import yfinance as yf


class PortfolioManager(Sujet):
    """Sujet concret : conserve l'état du portefeuille et notifie ses observateurs."""

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
            "MSFT": {
                "quantite": 8,
                "seuil_haut": 430.0,
                "seuil_bas": 380.0,
                "prix_courant": None,
                "ouverture": None,
            },
        }

    def recuperer_prix(self, ticker):
        """Retourne le prix actuel et le prix d'ouverture d'un titre."""
        info = yf.Ticker(ticker).fast_info
        prix = info["last_price"]
        ouverture = info["open"]

        if prix is None or ouverture is None:
            raise ValueError(f"Le titre '{ticker}' n'existe pas ou son prix est indisponible.")

        return prix, ouverture

    def rafraichir_prix(self):
        """Met à jour les prix de tous les titres, puis notifie les observateurs."""
        for ticker, infos in self._titres.items():
            prix, ouverture = self.recuperer_prix(ticker)
            infos["prix_courant"] = prix
            infos["ouverture"] = ouverture

        self.notifier()

    def ajouter_titre(self, ticker, quantite, seuil_bas=None, seuil_haut=None):
        """Ajoute un titre et notifie les observateurs."""
        ticker = ticker.strip().upper()

        if not ticker:
            raise ValueError("Le ticker est obligatoire.")
        if ticker in self._titres:
            raise ValueError(f"{ticker} existe déjà dans le portfolio.")
        if quantite <= 0:
            raise ValueError("La quantité doit être positive.")

        prix, ouverture = self.recuperer_prix(ticker)

        

        # Seuils facultatifs : ±20 % du prix actuel s'ils ne sont pas fournis.
        if seuil_bas is None:
            seuil_bas = round(prix * 0.8, 2)
        if seuil_haut is None:
            seuil_haut = round(prix * 1.2, 2)

        if seuil_bas <= 0 or seuil_haut <= 0:
            raise ValueError("Les seuils doivent être positifs.")
        if seuil_bas >= seuil_haut:
            raise ValueError("Le seuil bas doit être inférieur au seuil haut.")
        if prix is None or ouverture is None:
            raise ValueError(f"Le ticker « {ticker} » n'existe pas.")

        self._titres[ticker] = {
            "quantite": quantite,
            "seuil_haut": seuil_haut,
            "seuil_bas": seuil_bas,
            "prix_courant": prix,
            "ouverture": ouverture,
        }

        self.notifier()

    def retirer_titre(self, ticker):
        """Retire un titre et notifie les observateurs."""
        if ticker not in self._titres:
            raise ValueError(f"{ticker} n'existe pas dans le portfolio.")

        del self._titres[ticker]
        self.notifier()

    def modifier_titre(self, ticker, quantite=None, seuil_bas=None, seuil_haut=None):
        """Modifie les données d'un titre et notifie les observateurs."""
        if ticker not in self._titres:
            raise ValueError(f"{ticker} n'existe pas dans le portfolio.")

        if quantite is None and seuil_bas is None and seuil_haut is None:
            raise ValueError("Aucune modification fournie.")

        if quantite is not None and quantite <= 0:
            raise ValueError("La quantité doit être positive.")

        # Les deux seuils doivent être fournis ensemble.
        if (seuil_bas is None) != (seuil_haut is None):
            raise ValueError("Les deux seuils doivent être fournis ensemble.")

        if seuil_bas is not None:
            if seuil_bas <= 0 or seuil_haut <= 0:
                raise ValueError("Les seuils doivent être positifs.")
            if seuil_bas >= seuil_haut:
                raise ValueError("Le seuil bas doit être inférieur au seuil haut.")

        infos = self._titres[ticker]

        if quantite is not None:
            infos["quantite"] = quantite
        if seuil_bas is not None:
            infos["seuil_bas"] = seuil_bas
            infos["seuil_haut"] = seuil_haut

        self.notifier()

    def get_donnees(self):
        """Retourne une copie des données destinées aux observateurs."""
        valeur_totale = 0
        valeur_ouverture = 0

        for infos in self._titres.values():
            if infos["prix_courant"] is not None:
                valeur_totale += infos["prix_courant"] * infos["quantite"]

            if infos["ouverture"] is not None:
                valeur_ouverture += infos["ouverture"] * infos["quantite"]

        return {
            "titres": {
                ticker: infos.copy()
                for ticker, infos in self._titres.items()
            },
            "valeur_totale": valeur_totale,
            "valeur_ouverture": valeur_ouverture,
        }