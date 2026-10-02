class GestionTitresController:
    """Contrôle la logique métier liée à la gestion du portefeuille."""

    def __init__(self, sujet):
        self._sujet = sujet

    def parse_ajout(self, ticker, texte_quantite, texte_bas, texte_haut):
        ticker_valide = (ticker or "").strip().upper()
        if not ticker_valide:
            raise ValueError("Le ticker est obligatoire.")

        quantite = self._parse_quantite(texte_quantite)
        seuil_bas, seuil_haut = self._parse_alertes(texte_bas, texte_haut)
        return ticker_valide, quantite, seuil_bas, seuil_haut

    def parse_modification(self, texte_quantite, texte_bas, texte_haut):
        quantite = self._parse_quantite(texte_quantite) if texte_quantite else None
        seuil_bas, seuil_haut = self._parse_alertes(texte_bas, texte_haut)
        return quantite, seuil_bas, seuil_haut

    def ajouter_titre(self, ticker, quantite, seuil_bas=None, seuil_haut=None):
        ticker_valide = (ticker or "").strip().upper()
        if not ticker_valide:
            raise ValueError("Le ticker est obligatoire.")

        quantite_valide = self._parse_quantite(quantite)
        seuil_bas_valide, seuil_haut_valide = self._normaliser_alertes(seuil_bas, seuil_haut)

        self._sujet.ajouter_titre(ticker_valide, quantite_valide, seuil_bas_valide, seuil_haut_valide)
        return f"{ticker_valide} ajouté au portfolio."

    def retirer_titre(self, ticker):
        self._sujet.retirer_titre(ticker)
        return f"{ticker} retiré du portfolio."

    def modifier_titre(self, ticker, quantite=None, seuil_bas=None, seuil_haut=None):
        if ticker is None:
            raise ValueError("Sélectionnez un titre à modifier.")

        quantite_valide = self._parse_quantite(quantite) if quantite is not None else None
        seuil_bas_valide, seuil_haut_valide = self._normaliser_alertes(seuil_bas, seuil_haut)

        self._sujet.modifier_titre(ticker, quantite_valide, seuil_bas_valide, seuil_haut_valide)
        return f"{ticker} mis à jour."

    def _parse_quantite(self, texte_quantite):
        if texte_quantite is None or texte_quantite == "":
            raise ValueError("La quantité est obligatoire.")

        try:
            quantite = int(texte_quantite)
        except ValueError as erreur:
            raise ValueError("La quantité doit être un entier positif.") from erreur

        if quantite <= 0:
            raise ValueError("La quantité doit être positive.")

        return quantite

    def _normaliser_alertes(self, seuil_bas, seuil_haut):
        if (seuil_bas is None) != (seuil_haut is None):
            raise ValueError("Les deux alertes doivent être fournies ensemble.")

        if seuil_bas is None and seuil_haut is None:
            return None, None

        try:
            seuil_bas_valide = float(seuil_bas)
            seuil_haut_valide = float(seuil_haut)
        except ValueError as erreur:
            raise ValueError("Les alertes doivent être des nombres valides.") from erreur

        if seuil_bas_valide <= 0 or seuil_haut_valide <= 0:
            raise ValueError("Les seuils doivent être positifs.")
        if seuil_bas_valide >= seuil_haut_valide:
            raise ValueError("Le seuil bas doit être inférieur au seuil haut.")

        return seuil_bas_valide, seuil_haut_valide

    def _parse_alertes(self, texte_bas, texte_haut):
        if bool(texte_bas) != bool(texte_haut):
            raise ValueError("Les deux alertes doivent être fournies ensemble.")

        if not texte_bas and not texte_haut:
            return None, None

        try:
            seuil_bas = float(texte_bas)
            seuil_haut = float(texte_haut)
        except ValueError as erreur:
            raise ValueError("Les alertes doivent être des nombres valides.") from erreur

        if seuil_bas <= 0 or seuil_haut <= 0:
            raise ValueError("Les seuils doivent être positifs.")
        if seuil_bas >= seuil_haut:
            raise ValueError("Le seuil bas doit être inférieur au seuil haut.")

        return seuil_bas, seuil_haut
