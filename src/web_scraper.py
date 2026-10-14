# type: ignore
import inspect
from collections.abc import Sequence

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from logger import Logger
from path_vars import DRIVER_PATH


class WebScraper(Logger):
    def __init__(self, url: str, time_to_wait: int, options: Sequence[str]) -> None:
        super().__init__()
        self.time_to_wait = time_to_wait
        self.url = url
        self.options = options
        self.browser = self.make_chrome_browser()
        self.browser.get(url)

    def whoami(self) -> str:
        return inspect.currentframe().f_back.f_code.co_name

    def msg_not_found(self, method_name: str, element: tuple[str, str]) -> str:
        return f"{method_name} - {element} not found, trying again"

    def msg_click_intercepted(self, method_name: str, element: tuple[str, str]) -> str:
        return f"{method_name} - {element} click element intercepted"

    def msg_timeout(self, method_name: str, element: tuple[str, str]) -> str:
        return f"{method_name} - {element} retrieve data timed out"

    def make_chrome_browser(self) -> webdriver:
        chrome_options = webdriver.ChromeOptions()

        if self.options is not None:
            for option in self.options:
                chrome_options.add_argument(option)

        chrome_service = Service(
            executable_path=str(DRIVER_PATH),
        )

        return webdriver.Chrome(service=chrome_service, options=chrome_options)

    def fill_input(self, field_id: tuple[str, str], input_text: str) -> None:
        try:
            WebDriverWait(self.browser, self.time_to_wait).until(
                ec.element_to_be_clickable(field_id)
            ).send_keys(input_text)
        except StaleElementReferenceException:
            self.log_error(self.msg_not_found(self.whoami(), field_id))
            self.fill_input(field_id, input_text)

    def clear_input(self, field_id: tuple[str, str]) -> None:
        try:
            WebDriverWait(self.browser, self.time_to_wait).until(
                ec.element_to_be_clickable(field_id)
            ).clear()
        except StaleElementReferenceException:
            self.log_error(self.msg_not_found(self.whoami(), field_id))
            self.clear_input(field_id)

    def click_element(self, btn_id: tuple[str, str]) -> None:
        try:
            WebDriverWait(self.browser, self.time_to_wait).until(
                ec.element_to_be_clickable(btn_id)
            ).click()
        except StaleElementReferenceException:
            self.log_error(self.msg_not_found(self.whoami(), btn_id))
            self.click_element(btn_id)
        except ElementClickInterceptedException:
            self.log_error(self.msg_click_intercepted(self.whoami(), btn_id))
            if self.not_found():
                self.click_element(btn_id)

    def switch_to_inner_frame(self, frames: list[tuple[str, str]]) -> None:
        for frame in frames:
            table_iframe = self.browser.find_element(*frame)
            self.browser.switch_to.frame(table_iframe)

    def _get_by_tag(self, tag: tuple[str, str]) -> None:
        try:
            return WebDriverWait(self.browser, self.time_to_wait).until(
                ec.presence_of_element_located(tag)
            )
        except StaleElementReferenceException:
            self.log_error(self.msg_not_found(self.whoami(), tag))
            self._get_by_tag(tag)

    def _get_table_td(self, table_field: tuple[str, str]) -> None:
        try:
            WebDriverWait(self.browser, self.time_to_wait).until(
                ec.presence_of_element_located(table_field)
            )
            self._get_by_tag((By.TAG_NAME, "table"))
            self._get_by_tag((By.TAG_NAME, "tbody"))
            self._get_by_tag((By.TAG_NAME, "tr"))
            self._get_by_tag((By.TAG_NAME, "td"))
        except StaleElementReferenceException:
            self.log_error(self.msg_not_found(self.whoami(), table_field))
            self._get_table_td(table_field)

    def get_description(
        self, table_field: tuple[str, str], description_field: tuple[str, str]
    ) -> str | None:
        self._get_table_td(table_field)
        try:
            return (
                WebDriverWait(self.browser, self.time_to_wait)
                .until(ec.presence_of_element_located(description_field))
                .text
            )
        except StaleElementReferenceException:
            self.log_error(self.msg_not_found(self.whoami(), description_field))
            self.get_description(table_field, description_field)
        except TimeoutException:
            self.log_error(self.msg_timeout(self.whoami(), description_field))
            if self.not_found():
                self.get_description(table_field, description_field)

    def get_price(
        self,
        table_field: str,
        price_field: tuple[str, str],
        price_value_field: tuple[str, str],
    ) -> str | None:
        self._get_table_td(table_field)
        try:
            price_table = WebDriverWait(self.browser, self.time_to_wait).until(
                ec.presence_of_element_located(price_field)
            )
            return price_table.find_element(*price_value_field).text
        except StaleElementReferenceException:
            self.log_error(self.msg_not_found(self.whoami(), price_field))
            self.get_price(table_field, price_field, price_value_field)
        except TimeoutException:
            self.log_error(self.msg_timeout(self.whoami(), price_field))
            if self.not_found():
                self.get_price(table_field, price_field, price_value_field)

    def not_found(self) -> bool:
        try:
            WebDriverWait(self.browser, 2).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="pt1:d8_ok"]/a'))
            ).click()
            return True  # noqa: TRY300
        except ElementClickInterceptedException:
            self.log_error(self.msg_click_intercepted(self.whoami(), "NOT FOUND POPUP"))
            self.not_found()
        except (
            TimeoutException,
            StaleElementReferenceException,
            ElementNotInteractableException,
        ):
            return False
