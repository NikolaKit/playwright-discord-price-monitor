Playwright Web Price Monitor \& Discord Notifier



Automated tracker built with Python and Playwright. Renders a page inside a headless Chromium browser, extracts live product pricing, and dispatches instant Discord embed alerts when a target threshold is met.



Features

\- Headless Browser Scraping: Uses `playwright.sync\_api` to handle JavaScript-rendered pages reliably.

\- Instant Discord Alerts: Sends clean, structured embed notifications via Discord Webhooks.

\- Resilient Loop: Built-in error handling so temporary network timeouts do not crash the monitor.

\- Secure Config: Keeps webhook credentials isolated in a local `.env` file.



Setup:





\-- Clone the repository and install dependencies:

&#x20;  ```bash

&#x20;  git clone https://github.com/NikolaKit/playwright-discord-price-monitor.git

&#x20;  cd playwright-discord-price-monitor

&#x20;  pip install -r requirements.txt

&#x20;  playwright install chromium



\-- Create a .env file in the root directory:

DISCORD\_WEBHOOK\_URL=https://discord.com/api/webhooks/your\_webhook\_here



\-- Run the monitor:

python main.py

