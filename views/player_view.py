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
            print("2. Update a player")
            print("3. Delete a player")
            print("4. List all players")
            print("5. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_player_flow()
            elif choice == "2":
                self.update_player_flow()
            elif choice == "3":
                self.delete_player_flow()
            elif choice == "4":
                self.list_players_flow()
            elif choice == "5":
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
        national_chess_id = input("National Chess ID (ex: AB12345): ")

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

    def update_player_flow(self):
        """
        Update the information of a player.
        """
        national_id = input("Enter player's national chess id :")
        print("Leave blank if you want to keep the current value.")
        new_last_name = input("Enter player's last name: ")
        new_first_name = input("Enter player's first name: ")
        new_birth_date = input("Enter player's birth date (YYYY-MM-DD):")
        self.controller.update_player(
            national_id,
            new_last_name or None,
            new_first_name or None,
            new_birth_date or None
        )


    def delete_player_flow(self):
        """
        Delete a player.
        """
        national_id = input("Enter player's national chess id :")
        self.controller.delete_player(national_id)
