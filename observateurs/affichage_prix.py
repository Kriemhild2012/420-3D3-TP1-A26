import tkinter as tk

from observateurs.observateur import Observateur


class AffichagePrix(Observateur):
    """Observateur qui affiche le prix actuel et les changements
    depuis l'ouverture pour chaque titre."""

    def __init__(self, main_window: tk.Tk, sujet):
        self._sujet = sujet

        self._frame = tk.LabelFrame(
            main_window,
            text="Prix en temps réel",
            padx=10,
            pady=10
        )
        self._frame.pack(fill=tk.X, padx=10, pady=5)

        self._frames_prix = {}
        self._labels_prix = {}

        self.actualiser(sujet)

    def actualiser(self, sujet):
        """Met à jour l'affichage des prix lorsque le sujet change."""

        self._sujet = sujet

        donnees = sujet.get_donnees()
        titres = donnees["titres"]

        for ticker in titres:
            if ticker not in self._labels_prix:
                self._creer_ligne_prix(ticker)

        for ticker in list(self._labels_prix):
            if ticker not in titres:
                self._frames_prix[ticker].destroy()
                del self._frames_prix[ticker]
                del self._labels_prix[ticker]

        for ticker, infos in titres.items():
            prix = infos["prix_courant"]
            ouverture = infos["ouverture"]

            if prix is None or ouverture is None:
                self._labels_prix[ticker].config(
                    text="Chargement..."
                )
                continue

            variation = ((prix - ouverture) / ouverture) * 100

            symbole = "▲" if variation >= 0 else "▼"
            couleur = "green" if variation >= 0 else "red"

            self._labels_prix[ticker].config(
                text=f"{prix:.2f} $  {symbole} {abs(variation):.2f} %",
                fg=couleur
            )

    def _creer_ligne_prix(self, ticker):
        """Crée une ligne d'affichage pour un titre."""

        frame = tk.Frame(self._frame)
        frame.pack(fill=tk.X, pady=2)

        tk.Label(
            frame,
            text=f"{ticker}:",
            width=8,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(side=tk.LEFT)

        label = tk.Label(
            frame,
            text="Chargement..."
        )
        label.pack(side=tk.LEFT)

        self._frames_prix[ticker] = frame
        self._labels_prix[ticker] = label