import os
from time import sleep

from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException

from file_handler import FileHandler
from path_vars import DOTENV_PATH
from scrap_vars import (
    DESC_FIELD,
    EMAIL_FIELD,
    EXACT_MATCH,
    FIRST_FRAME,
    NEXT_BUTTON,
    NO_BUTTON,
    PRICE_FIELD,
    PRICE_VALUE_FIELD,
    SEARCH_BTN,
    SEARCH_INPUT,
    SECOND_FRAME,
    TABLE_DIV,
    X_BUTTON,
)
from web_scraper import WebScraper

if __name__ == "__main__":
    # .env
    load_dotenv(DOTENV_PATH)
    URL = os.environ.get("URL", ".env var not found, check your env file")
    USER = os.environ.get("USER", ".env var not found, check your env file")
    PASSWORD = os.environ.get("PASSWORD", ".env var not found, check your env file")

    # CSV Handler
    file_handler = FileHandler()
    PN_LIST = file_handler.get_pn_list()  # reads root.csv
    counter = file_handler.counter  # get current searched PN

    # Web scraping variables (Selenium)
    TIME_TO_WAIT = 60  # Time limit between each interaction (Timeout)

    # webdriver setup
    options = ("start-maximized", "incognito")  # opens on maximized screen
    web_scraper = WebScraper(URL, TIME_TO_WAIT, options)

    # Login session
    web_scraper.fill_input(EMAIL_FIELD, USER)  # fill email
    web_scraper.click_element(NEXT_BUTTON)  # click Next

    # Wait for authenticator check
    sleep(TIME_TO_WAIT)

    web_scraper.click_element(NO_BUTTON)  # click No
    web_scraper.click_element(X_BUTTON)  # click X on popup

    # Web scraping
    # focus on the inner HTML that contains the table used for scraping
    web_scraper.switch_to_inner_frame([FIRST_FRAME, SECOND_FRAME])
    # setup exact match to filter only one product at a time
    web_scraper.click_element(EXACT_MATCH)

    # Web scraping loop
    for pn in PN_LIST[counter:]:
        web_scraper.clear_input(SEARCH_INPUT)
        web_scraper.fill_input(SEARCH_INPUT, pn)
        web_scraper.click_element(SEARCH_BTN)
        pn = int(pn)

        # check if not found popup appears in the screen
        if web_scraper.not_found():
            file_handler.add_count(pn)
            file_handler.add_not_found_count(pn)
            continue

        # handles some timeout exceptions that occur when there are page delays
        try:
            description = web_scraper.get_description(TABLE_DIV, DESC_FIELD)
            price = web_scraper.get_price(TABLE_DIV, PRICE_FIELD, PRICE_VALUE_FIELD)  # type: ignore

            if price is None or description is None:
                file_handler.add_count(pn)
                file_handler.add_not_found_count(pn)
                continue

            price = price.replace(",", "")
            file_handler.update_csv([str(pn), description, price])
            file_handler.add_count(pn)

        except TimeoutException:
            web_scraper.not_found()
            file_handler.add_not_found_count(pn)

    file_handler.csv_to_excel()
