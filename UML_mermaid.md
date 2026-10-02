# UML du refactoring

Le sujet concret contient l'etat et les regles du portefeuille. Les observateurs
ne modifient jamais directement le portefeuille : ils lisent les donnees avec
`get_donnees()` et appellent les operations publiques du sujet pour transmettre
les actions de l'utilisateur.

```mermaid
classDiagram
	class Sujet {
		<<interface>>
		-_observateurs : list
		+abonner(observateur) void
		+desabonner(observateur) void
		+notifier() void
		+get_donnees() dict
	}

	class Observateur {
		<<interface>>
		+actualiser(sujet) void
	}

	class PortfolioManager {
		-_titres : dict
		+recuperer_prix(ticker) tuple
		+rafraichir_prix() void
		+ajouter_titre(ticker, quantite, seuil_bas, seuil_haut) void
		+retirer_titre(ticker) void
		+modifier_titre(ticker, quantite, seuil_bas, seuil_haut) void
		+get_donnees() dict
	}

	class AffichagePrix {
		-_frame : Frame
		-_labels_prix : dict
		+actualiser(sujet) void
	}

	class AffichageManagerTitres {
		-_frame : LabelFrame
		-_sujet : PortfolioManager
		+construire_gestion() void
		+actualiser(sujet) void
		+ajouter_titre() void
		+retirer_titre() void
		+modifier_selection() void
	}

	class AffichagePortfolio {
		-_label_valeur : Label
		-_label_variation : Label
		+actualiser(sujet) void
	}

	class AffichageAlertes {
		-_label_alertes : Label
		+actualiser(sujet) void
	}

	class JournalisationCSV {
		-_chemin : str
		+actualiser(sujet) void
	}

	class App {
		-_fenetre : Tk
		-_sujet : PortfolioManager
		+demarrer() void
	}

	Sujet <|.. PortfolioManager
	Observateur <|.. AffichagePrix
	Observateur <|.. AffichageManagerTitres
	Observateur <|.. AffichagePortfolio
	Observateur <|.. AffichageAlertes
	Observateur <|.. JournalisationCSV

	Sujet o-- Observateur : abonne
	App --> PortfolioManager : cree et utilise
	App --> AffichagePrix : cree
	App --> AffichageManagerTitres : cree
	App --> AffichagePortfolio : cree
	App --> AffichageAlertes : cree
	App --> JournalisationCSV : cree
	AffichageManagerTitres --> PortfolioManager : ajoute/modifie/retire
```

## Responsabilites

### `Sujet`

Interface fournie. Elle gere la liste des observateurs, leur abonnement et la
notification. Elle ne connait pas les details de Tkinter.

### `PortfolioManager`

Sujet concret. Il est responsable de l'etat du portefeuille, de la recuperation
des prix, de l'ajout, du retrait et de la modification des titres. Il appelle
`notifier()` apres chaque changement important.

### Observateurs visuels

- `AffichagePrix` affiche le prix et la variation de chaque titre.
- `AffichageManagerTitres` construit le formulaire et delegue les actions au
  `PortfolioManager`.
- `AffichagePortfolio` affiche la valeur totale et sa variation.
- `AffichageAlertes` affiche les titres qui ont franchi un seuil.

### Observateur non visuel

`JournalisationCSV` enregistre les donnees recues dans `portfolio.csv`. Il
respecte la contrainte d'au moins un observateur non visuel.

### `App`

Point d'assemblage de l'application. Elle cree la fenetre, le sujet et les
observateurs, puis abonne chaque observateur au `PortfolioManager`. Elle ne
calcule pas les prix et ne modifie pas directement `_titres`.

## Flux d'une mise a jour

```text
App -> PortfolioManager.rafraichir_prix()
PortfolioManager -> yfinance : recuperer les prix
PortfolioManager -> notifier()
notifier() -> AffichagePrix.actualiser()
notifier() -> AffichagePortfolio.actualiser()
notifier() -> AffichageAlertes.actualiser()
notifier() -> JournalisationCSV.actualiser()
```