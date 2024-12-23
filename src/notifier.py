import requests
import logging
from src.config import WEBHOOK_URL, ROLE_ID
from datetime import datetime


def format_discord_timestamp(iso_timestamp):
    """
    Converts an ISO 8601 timestamp into a Discord-supported `<t:epoch:format>` format.
    """
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))  # Convert ISO to datetime
    epoch = int(dt.timestamp())  # Convert to UNIX epoch
    return f"<t:{epoch}:F>"  # Use the `F` format for full date/time

def send_webhook_notification(game_title, game_status, start_date, end_date, link=None, image_url=None, is_current_game=True):
    """
    Sends an embedded notification to the configured Discord webhook about the free games on Epic Games Store.
    """
    # Message content
    if is_current_game:
        content = f"<@&{ROLE_ID}> 🎮 **{game_title}** is now free on Epic Games Store! Go grab it! 🎉"
    else:
        content = f"🕒 Get ready! **{game_title}** will be free soon on Epic Games Store!"

    # Construct the embed
    embed = {
        "title": game_title,
        "url": link,
        "description": f"Status: **{game_status}**",
        "color": 3447003,  # Blue color
        "fields": [],
        "footer": {"text": "Epic Games Free Games Notification"},
    }

    # Add start and end dates if available
    if start_date:
        embed["fields"].append({"name": "Start Date", "value": format_discord_timestamp(start_date), "inline": True})
    if end_date:
        embed["fields"].append({"name": "End Date", "value": format_discord_timestamp(end_date), "inline": True})

    # Add the image to the embed if available
    if image_url:
        embed["image"] = {"url": image_url}

    data = {
        "content": content,  # Notification content
        "embeds": [embed],
    }

    # Send the notification to Discord
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            logging.info(f"Notification sent successfully for {game_title}!")
        else:
            logging.error(f"Failed to send notification for {game_title}. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending notification: {e}")