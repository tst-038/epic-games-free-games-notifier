import logging
import os
import time
from src.scraper import get_latest_free_games
from src.notifier import send_webhook_notification
from src.config import CHECK_INTERVAL

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# File to store the last game's title and status
LAST_GAME_FILE = "last_game.txt"

def read_last_game():
    """
    Reads the last game's details (title and status) from a file.
    """
    if os.path.exists(LAST_GAME_FILE):
        with open(LAST_GAME_FILE, "r") as file:
            return file.read().strip().split(",")
    return None, None

def write_last_game(title, status):
    """
    Writes the current game's details (title and status) to the file.
    """
    with open(LAST_GAME_FILE, "w") as file:
        file.write(f"{title},{status}")

def main():
    logging.info("Starting Epic Games Free Games Notifier...")

    while True:
        games_data = get_latest_free_games()
        if games_data and "current_game" in games_data:
            current_game = games_data["current_game"]
            last_title, last_status = read_last_game()

            # Compare the current game with the last game
            if current_game["title"] != last_title or current_game["status"] != last_status:
                logging.info(f"New or updated game found: {current_game['title']} ({current_game['status']})")
                send_webhook_notification(
                    current_game["title"],
                    current_game["status"],
                    current_game.get("start_date"),
                    current_game.get("end_date"),
                    current_game["link"],
                    current_game.get("image_url"),
                )
                write_last_game(current_game["title"], current_game["status"])
            else:
                logging.info(
                    f"No updates. Current game: {current_game['title']}, status: {current_game['status']}"
                )
        else:
            logging.error("No game data returned.")

        # Wait for the configured interval before checking again
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()