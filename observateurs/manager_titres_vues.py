import tkinter as tk
from views.styles import POLICE_PETITE, POLICE_STATUT
from observateurs.manager_titres import GestionTitresController
from observateurs.observateur import Observateur


class GestionTitresView(Observateur):
    def __init__(self, main_window: tk.Tk, sujet):
        self._sujet = sujet
        self._controleur = GestionTitresController(sujet)
        self._frame = tk.LabelFrame(main_window, text="Gérer les titres", padx=10, pady=10)
        self._frame.pack(fill=tk.X, padx=10, pady=5)
        self.construire_gestion()
        self.actualiser(sujet)

    def actualiser(self, sujet):
        self._sujet = sujet
        self._controleur = GestionTitresController(sujet)
        donnees = sujet.get_donnees()
        titres = donnees["titres"]

        self.listbox_titres.delete(0, tk.END)
        for ticker in titres:
            self.listbox_titres.insert(tk.END, self._texte_listbox(ticker, titres))

    def construire_gestion(self):
        ligne_ajout = tk.Frame(self._frame)
        ligne_ajout.pack(fill=tk.X)
        self.entry_ticker = self._champ(ligne_ajout, "Ticker", width=8)
        self.entry_quantite = self._champ(ligne_ajout, "Qté", width=5, valeur_defaut="1")
        self.entry_seuil_bas_ajout = self._champ(ligne_ajout, "Alerte basse", width=7)
        self.entry_seuil_haut_ajout = self._champ(ligne_ajout, "Alerte haute", width=7)
        tk.Button(ligne_ajout, text="Ajouter", command=self.ajouter_titre).pack(side=tk.LEFT)

        tk.Label(
            self._frame,
            text="(Alertes optionnelles : si vides, calculées à ±20% du prix actuel)",
            font=POLICE_PETITE
        ).pack(anchor="w", pady=(2, 5))

        ligne_liste = tk.Frame(self._frame)
        ligne_liste.pack(fill=tk.X)
        self.listbox_titres = tk.Listbox(ligne_liste, height=4, exportselection=False)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(ligne_liste, text="Retirer", command=self.retirer_titre).pack(side=tk.LEFT, padx=(5, 0), anchor="n")

        ligne_modif = tk.Frame(self._frame)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))
        tk.Label(ligne_modif, text="Sélection →").pack(side=tk.LEFT)
        self.entry_nouvelle_quantite = self._champ(ligne_modif, "Qté", width=5)
        self.entry_nouveau_seuil_bas = self._champ(ligne_modif, "Alerte basse", width=7)
        self.entry_nouveau_seuil_haut = self._champ(ligne_modif, "Alerte haute", width=7)
        tk.Button(ligne_modif, text="Modifier sélection", command=self.modifier_selection).pack(side=tk.LEFT)

        self._label_statut_titres = tk.Label(self._frame, text="", font=POLICE_STATUT, fg="gray")
        self._label_statut_titres.pack(anchor="w", pady=(5, 0))

    def _champ(self, parent, texte, width, valeur_defaut=""):
        tk.Label(parent, text=f"{texte}:").pack(side=tk.LEFT)
        entry = tk.Entry(parent, width=width)
        if valeur_defaut:
            entry.insert(0, valeur_defaut)
        entry.pack(side=tk.LEFT, padx=(2, 8))
        return entry

    def _texte_listbox(self, ticker, titres):
        infos = titres[ticker]
        return (
            f"{ticker} — {infos['quantite']} action(s) "
            f"(alerte : {infos['seuil_bas']:.2f} $ / {infos['seuil_haut']:.2f} $)"
        )

    def _ticker_selectionne(self):
        selection = self.listbox_titres.curselection()
        if not selection:
            return None
        texte = self.listbox_titres.get(selection[0])
        return texte.split(" — ")[0]

    def _statut(self, texte, couleur):
        self._label_statut_titres.config(text=texte, fg=couleur)

    def ajouter_titre(self):
        try:
            ticker, quantite, seuil_bas, seuil_haut = self._controleur.parse_ajout(
                self.entry_ticker.get(),
                self.entry_quantite.get(),
                self.entry_seuil_bas_ajout.get(),
                self.entry_seuil_haut_ajout.get(),
            )
            message = self._controleur.ajouter_titre(ticker, quantite, seuil_bas, seuil_haut)
        except ValueError as erreur:
            self._statut(str(erreur), "red")
            return
        except Exception:
            self._statut("Impossible de récupérer les données du ticker.", "red")
            return

        self._vider_champs(
            self.entry_ticker,
            self.entry_quantite,
            self.entry_seuil_bas_ajout,
            self.entry_seuil_haut_ajout,
        )
        self.entry_quantite.insert(0, "1")
        self._statut(message, "green")

    def retirer_titre(self):
        ticker = self._ticker_selectionne()
        if ticker is None:
            self._statut("Sélectionnez un titre à retirer.", "orange")
            return

        try:
            message = self._controleur.retirer_titre(ticker)
        except ValueError as erreur:
            self._statut(str(erreur), "red")
            return

        self._statut(message, "gray")

    def modifier_selection(self):
        ticker = self._ticker_selectionne()
        if ticker is None:
            self._statut("Sélectionnez un titre à modifier.", "orange")
            return

        try:
            quantite, seuil_bas, seuil_haut = self._controleur.parse_modification(
                self.entry_nouvelle_quantite.get(),
                self.entry_nouveau_seuil_bas.get(),
                self.entry_nouveau_seuil_haut.get(),
            )
            message = self._controleur.modifier_titre(ticker, quantite, seuil_bas, seuil_haut)
        except ValueError as erreur:
            self._statut(str(erreur), "red")
            return

        self._vider_champs(
            self.entry_nouvelle_quantite,
            self.entry_nouveau_seuil_bas,
            self.entry_nouveau_seuil_haut,
        )
        self._statut(message, "green")

    def _vider_champs(self, *champs):
        for champ in champs:
            champ.delete(0, tk.END)
