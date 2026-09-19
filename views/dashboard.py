import tkinter as tk
from views.styles import POLICE
from modeles.portfolio_manager import PortfolioManager
from observateurs.manager_titres import GestionTitresView
from observateurs.logger_CSV import LoggerCSV

INTERVALLE_MS = 30000  # Fréquence de rafraîchissement des prix (30 secondes)

class Dashboard(tk.Tk):
    """Fenêtre principale minimale, utilisée pour tester le sujet et son observateur."""

    def __init__(self):
        super().__init__()

        self.title("Portfolio Tracker")
        self.resizable(False, False)
        self.option_add("*Font", POLICE)

        # Création du Sujet
        self.portfolio_manager = PortfolioManager()

        # Création des Observateurs
        self.affichage_manager_titres = GestionTitresView(
            self,
            self.portfolio_manager,
        )
        self.logger_csv = LoggerCSV(self.portfolio_manager)

        # Abonnement des Observateurs au Sujet
        self.portfolio_manager.abonner(self.affichage_manager_titres)
        self.portfolio_manager.abonner(self.logger_csv)

        # Lance le premier cycle dès que Tkinter démarre.
        self.after(0, self.rafraichir_prix)

    def rafraichir_prix(self):
        try:
            self.portfolio_manager.rafraichir_prix()
        except Exception as erreur:
            print(f"Erreur de mise à jour des prix : {erreur}")
        finally:
            # Programme le cycle suivant, même après une erreur réseau.
            self.after(INTERVALLE_MS, self.rafraichir_prix)


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.mainloop()