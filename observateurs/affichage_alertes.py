from observateurs.observateur import Observateur
import tkinter as tk


class AffichageAlertes(Observateur):
    """Observateur qui affiche les alertes lorsque les prix
    dépassent les seuils configurés."""

    def __init__(self, main_window: tk.Tk, sujet):
        self._sujet = sujet

        self._frame = tk.LabelFrame(
            main_window,
            text="Alertes",
            padx=10,
            pady=10
        )
        self._frame.pack(fill=tk.X, padx=10, pady=5)

        self._label_alertes = tk.Label(
            self._frame,
            text="Aucune alerte",
            fg="gray",
            justify=tk.LEFT,
            wraplength=380
        )
        self._label_alertes.pack(anchor="w")

        # Premier affichage
        self.actualiser(sujet)

    def actualiser(self, sujet):
        """Vérifie les seuils et met à jour l'affichage des alertes."""

        self._sujet = sujet

        donnees = sujet.get_donnees()
        titres = donnees["titres"]

        alertes = []

        for ticker, infos in titres.items():

            prix = infos["prix_courant"]
            seuil_haut = infos["seuil_haut"]
            seuil_bas = infos["seuil_bas"]

            # Le prix peut être None au démarrage
            if prix is None:
                continue

            if prix >= seuil_haut:
                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut "
                    f"({prix:.2f} $ ≥ {seuil_haut:.2f} $)"
                )

            elif prix <= seuil_bas:
                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas "
                    f"({prix:.2f} $ ≤ {seuil_bas:.2f} $)"
                )

        if alertes:
            self._label_alertes.config(
                text="\n".join(alertes),
                fg="red"
            )
        else:
            self._label_alertes.config(
                text="Aucune alerte",
                fg="gray"
            )