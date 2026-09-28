from observateurs.observateur import Observateur
import tkinter as tk


class AffichagePortfolio(Observateur):
    """Observateur qui affiche la valeur totale du portfolio
    et sa variation depuis l'ouverture."""

    def __init__(self, main_window: tk.Tk, sujet):
        self._sujet = sujet

        self._frame = tk.LabelFrame(
            main_window,
            text="Mon portfolio",
            padx=10,
            pady=10
        )
        self._frame.pack(fill=tk.X, padx=10, pady=5)

        self._label_valeur = tk.Label(
            self._frame,
            text="Valeur totale : calcul en cours...",
            font=("Segoe UI", 13, "bold")
        )
        self._label_valeur.pack()

        self._label_variation = tk.Label(
            self._frame,
            text=""
        )
        self._label_variation.pack()

        # Premier affichage
        self.actualiser(sujet)

    def actualiser(self, sujet):
        """Met à jour l'affichage du portfolio lorsque le sujet change."""

        self._sujet = sujet

        donnees = sujet.get_donnees()

        valeur_totale = donnees["valeur_totale"]
        valeur_ouverture = donnees["valeur_ouverture"]

        variation = valeur_totale - valeur_ouverture

        self._label_valeur.config(
            text=f"Valeur totale : {valeur_totale:.2f} $"
        )

        symbole = "▲" if variation >= 0 else "▼"

        couleur = "green" if variation >= 0 else "red"

        self._label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg=couleur
        )