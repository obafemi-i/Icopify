### Icopify scraper

The scraper uses Playwright to login and maintain the session to go through pages.
Also uses Selectolax to parse the needed HTML.

The first command to install the needed libraries, the second command to install the playwright browsers.
- > pip install -r requirements.txt
- > playwright install

Icopify credentials (email and password) should be in a creds.py file which is imported into the main.py file on line 5.

