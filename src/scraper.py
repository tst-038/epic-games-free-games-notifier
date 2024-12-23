import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from src.config import DROP_URL


def get_page_content_with_playwright(url):
    """
    Fetches the HTML content of the given URL using Playwright with a custom user agent.
    """
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)

        # Create a new browser context with a custom user agent
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            )
        )

        # Open a new page in the context
        page = context.new_page()

        # Navigate to the URL
        page.goto(url)

        # Wait for the page to load completely
        page.wait_for_selector('div[data-testid="picture"] img')

        # Get the page content
        html_content = page.content()

        # Close the browser
        browser.close()

        return html_content


def get_latest_free_games():
    """
    Scrapes the Epic Games free games page and extracts the current and next free games.
    """
    # Get rendered HTML content
    html_content = get_page_content_with_playwright(DROP_URL)
    soup = BeautifulSoup(html_content, "html.parser")

    current_game = {}
    next_game = {}

    # Find all offer cards
    offer_cards = soup.select('div[data-component="VaultOfferCard"]')

    for card in offer_cards:
        title_tag = card.select_one("h6")
        status_tag = card.select_one("span")
        img_tag = card.select_one('div[data-testid="picture"] img')  # Adjust to target img inside the div
        link_tag = card.find("a", href=True)
        time_tag = card.select_one("time")

        title = title_tag.text.strip() if title_tag else "Unknown Game"
        status = status_tag.text.strip() if status_tag else "Unknown Status"
        image_url = img_tag["data-image"].replace('&amp;', '&') if img_tag else None
        link = f"https://store.epicgames.com{link_tag['href']}" if link_tag else DROP_URL
        end_date = time_tag["datetime"] if time_tag else None

        if "Free Now" in status:
            current_game = {
                "title": title,
                "status": status,
                "start_date": None,  # Epic does not display a start date for "Free Now"
                "end_date": end_date,  # Needs manual check or scraping
                "image_url": image_url,
                "link": link,
            }
        elif "Unlocking in" in status:
            next_game = {
                "title": title,
                "status": status,
                "start_date": None,  # Could extract from the timer if provided
                "end_date": None,
                "image_url": image_url,
                "link": link,
            }

    return {"current_game": current_game, "next_game": next_game}