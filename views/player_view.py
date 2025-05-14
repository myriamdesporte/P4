"""Define the player view."""

from controllers.player_controller import PlayerController


class PlayerView:
    def __init__(self):
        """
        Initialize the view with a PlayerController instance.
        """
        self.controller = PlayerController()

    def display_menu(self):
        """
        Display the main menu and route user choices to corresponding actions.
        """
        while True:
            print("\nChess Tournament - Player Management")
            print("1. Add a new player")
            print("2. List all players")
            print("3. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_player_flow()
            elif choice == "2":
                self.list_players_flow()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_player_flow(self):
        """
        Prompt the user to enter information for a new player
        and delegate player creation to the controller.
        """
        print("\nEnter player information:")
        last_name = input("Last name: ")
        first_name = input("First name: ")
        birth_date = input("Birth date (YYYY-MM-DD): ")
        national_chess_id = input("National Chess ID (e.g., AB12345): ")

        player = self.controller.create_player(
            last_name, first_name, birth_date, national_chess_id
        )
        print(f"\nPlayer {player.first_name} {player.last_name} "
              f"has been added.")

    def list_players_flow(self):
        """
        Display all saved players from the controller.
        """
        print("\nList of all players:")
        players = self.controller.list_players()
        if not players:
            print("No players found.")
        for player in players:
            print(f"- {player}")
