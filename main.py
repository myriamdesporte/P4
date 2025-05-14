"""Entry point."""

from controllers.player_controller import PlayerController


def main():
    controller = PlayerController()

    # Création de deux joueurs via le contrôleur
    try:
        controller.create_player("Doe", "John", "2000-01-01", "AB12345")
        controller.create_player("Dupont", "Jean", "2000-02-01", "CD67890")
    except ValueError as e:
        print(f"[Erreur] {e}")

    # Affichage de tous les joueurs
    print("\nListe des joueurs enregistrés :")
    for player in controller.list_players():
        print(player)


if __name__ == "__main__":
    main()
