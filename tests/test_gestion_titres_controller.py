import unittest

from observateurs.manager_titres import GestionTitresController


class DummySujet:
    def __init__(self):
        self.titres = {}

    def ajouter_titre(self, ticker, quantite, seuil_bas=None, seuil_haut=None):
        self.titres[ticker] = {
            "quantite": quantite,
            "seuil_bas": seuil_bas,
            "seuil_haut": seuil_haut,
        }

    def retirer_titre(self, ticker):
        self.titres.pop(ticker)

    def modifier_titre(self, ticker, quantite=None, seuil_bas=None, seuil_haut=None):
        if ticker not in self.titres:
            raise ValueError(f"{ticker} n'existe pas dans le portfolio.")
        if quantite is not None:
            self.titres[ticker]["quantite"] = quantite
        if seuil_bas is not None:
            self.titres[ticker]["seuil_bas"] = seuil_bas
            self.titres[ticker]["seuil_haut"] = seuil_haut


class GestionTitresControllerTests(unittest.TestCase):
    def test_ajout_valide_avec_alertes_automatiques(self):
        sujet = DummySujet()
        controller = GestionTitresController(sujet)

        resultat = controller.ajouter_titre("AAPL", 10, None, None)

        self.assertEqual(resultat, "AAPL ajouté au portfolio.")
        self.assertIn("AAPL", sujet.titres)

    def test_modification_rejette_seuils_incoherents(self):
        sujet = DummySujet()
        sujet.titres["AAPL"] = {"quantite": 5, "seuil_bas": 10.0, "seuil_haut": 20.0}
        controller = GestionTitresController(sujet)

        with self.assertRaises(ValueError):
            controller.modifier_titre("AAPL", quantite=7, seuil_bas=30.0, seuil_haut=20.0)


if __name__ == "__main__":
    unittest.main()
