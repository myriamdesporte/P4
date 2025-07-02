import os
import re
import webbrowser
from infra.repositories.json_player_repository import JSONPlayerRepository

TEMPLATE_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "templates", "players_report.html")
)

GENERATED_REPORT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "players_report_generated.html"
)

def generate_player_report():
    """
    Generate an HTML report of all players and open it in the default web browser.
    """
    repository = JSONPlayerRepository()
    players = repository.load_players()

    rows = ""
    for player in players:
        rows += f"""
        <tr>
            <td>{player.last_name}</td>
            <td>{player.first_name}</td>
            <td>{player.birth_date}</td>
            <td>{player.national_chess_id}</td>
        </tr>
        """

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        html_content = file.read()

    updated_html = re.sub(
        r"(<tbody>)(.*?)(</tbody>)",
        rf"\1{rows}\3",
        html_content,
        flags=re.DOTALL
    )

    with open(GENERATED_REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(updated_html)

    webbrowser.open(f"file://{GENERATED_REPORT_PATH}")