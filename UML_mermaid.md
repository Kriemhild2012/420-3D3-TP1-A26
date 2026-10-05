classDiagram
    direction LR

    %% --- modeles/ ---
    class Sujet {
        <<abstract>>
        -_observateurs list
        +abonner(observateur)
        +desabonner(observateur)
        +notifier()
        +get_donnees() dict*
    }

    class PortfolioManager {
        -_titres dict
        +recuperer_prix(ticker) tuple
        +rafraichir_prix()
        +ajouter_titre(ticker, quantite, seuil_bas, seuil_haut)
        +retirer_titre(ticker)
        +modifier_titre(ticker, quantite, seuil_bas, seuil_haut)
        +get_donnees() dict
    }

    %% --- observateurs/ ---
    class Observateur {
        <<abstract>>
        +actualiser(sujet)*
    }

    class AffichagePrix {
        -_frame
        -_frames_prix dict
        -_labels_prix dict
        +actualiser(sujet)
        -_creer_ligne_prix(ticker)
    }

    class AffichagePortfolio {
        -_label_valeur
        -_label_variation
        +actualiser(sujet)
    }

    class AffichageAlertes {
        -_label_alertes
        +actualiser(sujet)
    }

    class LoggerCSV {
        -_nom_fichier str
        +actualiser(sujet)
        +ecriture(titres)
    }

    class GestionTitresView {
        -_controleur GestionTitresController
        -listbox_titres
        +actualiser(sujet)
        +construire_gestion()
        +ajouter_titre()
        +retirer_titre()
        +modifier_selection()
    }

    class GestionTitresController {
        -_sujet
        +parse_ajout(ticker, qte, bas, haut) tuple
        +parse_modification(qte, bas, haut) tuple
        +ajouter_titre(ticker, quantite, seuil_bas, seuil_haut) str
        +retirer_titre(ticker) str
        +modifier_titre(ticker, quantite, seuil_bas, seuil_haut) str
    }

    %% --- racine : dashboard.py ---
    class Dashboard {
        <<tk.Tk>>
        +portfolio_manager PortfolioManager
        +rafraichir_prix()
    }

    Sujet <|-- PortfolioManager
    Observateur <|-- AffichagePrix
    Observateur <|-- AffichagePortfolio
    Observateur <|-- AffichageAlertes
    Observateur <|-- LoggerCSV
    Observateur <|-- GestionTitresView

    Sujet "1" o-- "many" Observateur : abonne
    GestionTitresView *-- GestionTitresController : crée
    GestionTitresController --> Sujet : appelle

    Dashboard *-- PortfolioManager
    Dashboard *-- AffichagePrix
    Dashboard *-- GestionTitresView
    Dashboard *-- LoggerCSV
    Dashboard *-- AffichagePortfolio
    Dashboard *-- AffichageAlertes
