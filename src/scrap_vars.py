from selenium.webdriver.common.by import By

# Web scrap variables
# Login
EMAIL_FIELD = (By.ID, "i0116")
PASSWORD_FIELD = (By.ID, "i0118")
NEXT_BUTTON = (By.ID, "idSIButton9")
NO_BUTTON = (By.ID, "idBtn_Back")
X_BUTTON = (By.ID, "dialogCloseIconButton_2")

# Iframes
FIRST_FRAME = (By.ID, "FullPageWebResource")  # first inner frame
# second frame that contains the scraping table
SECOND_FRAME = (By.ID, "kesteQuoteIframe")

# Data table
SEARCH_INPUT = (By.ID, "pt1:it1::content")
EXACT_MATCH = (By.ID, "pt1:sbc1::content")  # exact match checkbox
SEARCH_BTN = (By.ID, "pt1:cb2")
TABLE_DIV = (By.ID, "pt1:pc1:t1::db")  # Div that contains a table inside
DESC_FIELD = (By.XPATH, '//*[@id="pt1:pc1:t1:0:c4"]/span')
PRICE_FIELD = (By.XPATH, '//*[@id="pt1:pc1:t1:0:c14"]/span')
PRICE_VALUE_FIELD = (By.XPATH, '//*[@id="pt1:pc1:t1:0:pgl9"]/tbody/tr/td[3]')
