from domain.models.tournament import Tournament
from domain.ports.player_repository import IPlayerRepository


def load_tournament_players_from_ids(
        tournament: Tournament,
        player_repository: IPlayerRepository
) -> None:
    loaded_players = []
    for player_id in tournament.players:
        player = player_repository.get_by_id(player_id)
        if player:
            loaded_players.append(player)
    tournament.players = loaded_players