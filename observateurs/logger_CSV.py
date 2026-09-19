from observateurs.observateur import Observateur
#from observateurs.affichage_alertes import AffichageAlertes
from datetime import datetime

class LoggerCSV(Observateur):
	def __init__(self, sujet):
		self._nom_fichier = "portfolio.csv"
		self._sujet = sujet

	def ecriture(self, titres):
		horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		with open(self._nom_fichier, "a") as fichier:
			for ticker, infos in titres.items():
				prix = infos["prix_courant"]
				ouverture = infos["ouverture"]

	            # Au démarrage, les prix ne sont pas encore chargés.
				if prix is None or ouverture is None:
					continue

				fichier.write(
	                f"{horodatage},{ticker},{prix:.2f},{ouverture:.2f}\n"
	            )

		#AffichageAlertes._label_maj.config(text=f"Dernière mise à jour : {horodatage}", fg="gray")

	def actualiser(self, sujet):
		self._sujet = sujet
		donnees = sujet.get_donnees()
		titres = donnees["titres"]
		self.ecriture(titres=titres)