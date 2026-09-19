from observateurs.observateur import Observateur
import tkinter as tk

class GestionTitresView(Observateur):
    def __init__(self, main_window: tk.Tk, sujet):
        self._sujet = sujet
        self._frame = tk.LabelFrame(main_window, text="Gérer les titres", padx=10, pady=10)
        self._frame.pack(fill=tk.X, padx=10, pady=5)
        self.construire_gestion()
        self.actualiser(sujet)
    
    def actualiser(self, sujet):
        self._sujet = sujet
        donnees = sujet.get_donnees()
        titres = donnees["titres"]

        self.listbox_titres.delete(0, tk.END)
        for ticker in titres:
            self.listbox_titres.insert(tk.END, self._texte_listbox(ticker, titres))

    def construire_gestion(self):
        # Ligne 1 : formulaire d'ajout d'un nouveau titre
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
            font=("Segoe UI", 8), fg="gray"
        ).pack(anchor="w", pady=(2, 5))
            
        # Ligne 2 : liste des titres actuellement dans le portefeuille + retrait
        # (la sélection dans cette liste sert aussi au formulaire de modification ci-dessous)
        ligne_liste = tk.Frame(self._frame)
        ligne_liste.pack(fill=tk.X)
        self.listbox_titres = tk.Listbox(ligne_liste, height=4, exportselection=False)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(ligne_liste, text="Retirer", command=self.retirer_titre).pack(side=tk.LEFT, padx=(5, 0), anchor="n")
            
        # Ligne 3 : modification de la quantité et/ou des seuils du titre sélectionné
        ligne_modif = tk.Frame(self._frame)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))
        tk.Label(ligne_modif, text="Sélection →").pack(side=tk.LEFT)
        self.entry_nouvelle_quantite = self._champ(ligne_modif, "Qté", width=5)
        self.entry_nouveau_seuil_bas = self._champ(ligne_modif, "Alerte basse", width=7)
        self.entry_nouveau_seuil_haut = self._champ(ligne_modif, "Alerte haute", width=7)
        tk.Button(ligne_modif, text="Modifier sélection", command=self.modifier_selection).pack(side=tk.LEFT)
            
        # Message de statut (succès / erreur) pour les actions de cette section
        self._label_statut_titres = tk.Label(self._frame, text="", font=("Segoe UI", 9), fg="gray")
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
        ticker = self.entry_ticker.get().strip().upper()
        texte_quantite = self.entry_quantite.get().strip()
        texte_bas = self.entry_seuil_bas_ajout.get().strip()
        texte_haut = self.entry_seuil_haut_ajout.get().strip()

        try:
            quantite = int(texte_quantite)

            if bool(texte_bas) != bool(texte_haut):
                raise ValueError("Les deux alertes doivent être fournies ensemble.")

            seuil_bas = float(texte_bas) if texte_bas else None
            seuil_haut = float(texte_haut) if texte_haut else None

            self._sujet.ajouter_titre(
                ticker,
                quantite,
                seuil_bas,
                seuil_haut,
            )

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
        self._statut(f"{ticker} ajouté au portfolio.", "green")

    def retirer_titre(self):
        ticker = self._ticker_selectionne()
        if ticker is None:
            self._statut("Sélectionnez un titre à retirer.", "orange")
            return

        try:
            self._sujet.retirer_titre(ticker)
        except ValueError as erreur:
            self._statut(str(erreur), "red")
            return

        self._statut(f"{ticker} retiré du portfolio.", "gray")

    def modifier_selection(self):
        ticker = self._ticker_selectionne()
        if ticker is None:
            self._statut("Sélectionnez un titre à modifier.", "orange")
            return

        quantite_texte = self.entry_nouvelle_quantite.get().strip()
        bas_texte = self.entry_nouveau_seuil_bas.get().strip()
        haut_texte = self.entry_nouveau_seuil_haut.get().strip()

        try:
            quantite = int(quantite_texte) if quantite_texte else None

            if bool(bas_texte) != bool(haut_texte):
                raise ValueError("Les deux alertes doivent être fournies ensemble.")

            seuil_bas = float(bas_texte) if bas_texte else None
            seuil_haut = float(haut_texte) if haut_texte else None

            self._sujet.modifier_titre(
                ticker,
                quantite,
                seuil_bas,
                seuil_haut,
            )

        except ValueError as erreur:
            self._statut(str(erreur), "red")
            return

        self._vider_champs(
            self.entry_nouvelle_quantite,
            self.entry_nouveau_seuil_bas,
            self.entry_nouveau_seuil_haut,
        )
        self._statut(f"{ticker} mis à jour.", "green")

    def _vider_champs(self, *champs):
        for champ in champs:
            champ.delete(0, tk.END)
