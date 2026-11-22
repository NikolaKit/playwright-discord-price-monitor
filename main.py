import os
import time
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright


load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
PRODUCT_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
TARGET_PRICE = 55.00
CHECK_INTERVAL = 60  # seconds between checks


def get_product_info(url: str) -> tuple[str, float]:

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)

        title = page.locator("div.product_main h1").inner_text().strip()
        raw_price = page.locator("p.price_color").inner_text().strip()
        price = float(raw_price.replace("£", "").replace("$", ""))

        browser.close()
        return title, price


def send_discord_alert(title: str, price: float, url: str) -> None:

    if not WEBHOOK_URL:
        print("[!] DISCORD_WEBHOOK_URL not configured in .env file.")
        return

    payload = {
        "embeds": [
            {
                "title": f"Price Drop Alert: {title}",
                "url": url,
                "color": 5763719,  # green color
                "fields": [
                    {"name": "Current Price", "value": f"£{price:.2f}", "inline": True},
                    {"name": "Target Price", "value": f"£{TARGET_PRICE:.2f}", "inline": True},
                ],
                "footer": {"text": "Playwright Price Monitor"},
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()


def main() -> None:
    print(f"Started monitoring for: {PRODUCT_URL}")
    while True:
        try:
            title, price = get_product_info(PRODUCT_URL)
            print(f"[OK] {title} -> £{price:.2f}")

            if price <= TARGET_PRICE:
                send_discord_alert(title, price, PRODUCT_URL)
                print("[+] Message sent on Discord. Stopping the script...")
                break

        except Exception as e:
            print(f"[Error]: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
