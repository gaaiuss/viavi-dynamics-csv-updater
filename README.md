# Update PNs Equip csv - \*_NOT WORKING DUE TO MS UPDATES!_

This is a script to update a CSV file based on another resource CSV. It uses
web scraping to log in to Dynamics via Selenium module to capture the table
values and write them to a new CSV file line by line.

## Basic Functionality

### Browser Login

- Gets the user, password, and Dynamics URL from a `.env` file.

- Uses Selenium and the `.env` variables for the login session.

- Captures the HTML elements by id, XPATH and tag to scrap the products data.

### Web Scraping

- All the interactions to get the data from the webpage are made via Selenium.

- The script uses the basic functions of selenium to achieve the inner table
  that is located in a iframe inside the page.

- Once it gets there, all the web scraping are made inside this table on a
  "for" loop, searching for each PN from the `root.csv` file.

- If the product is located, the script scraps the specified fields and writes
  the information on a new file: `output\Updated_PNs_Equipments.csv`. If the product is
  not found, the loop continues with the next PN number.

### Error handling

- Sometimes Selenium does not find an HTML element on the first try, so a new
  interaction is made if that occurs. This can cause an infinite loop if an
  element ID is wrong or changed.

- Not found case: Selenium clicks on the "OK" button popup and simply continues
  the loop.

- System processing: Sometimes the system pops up a warning message, the script
  awaits the warning to clear to continue the loop.

- Timeout, click obtrusion: Sometimes a HTML element cannot be found or clicked
  due to a system delay, the script simply tries the current action again to
  mitigate the current error involving this problem.

## Setup

- Install the requirements:

```python
pip install -r requirements.txt
```

- Change the variables in `.env_example`.

- Rename the file to `.env`.

- Run the `src\main.py` file:

```python
python .\src\main.py
```

- The script runs in background and saves the current PN that it is searching
  for, so you can minimize it or screen lock it if you want.
