from datetime import datetime
from pathlib import Path

TIME_NOW = datetime.now().strftime("%Y%m%d_%H%M%S")
ROOT_DIR = Path(__file__).parent.parent

# Resources
RESOURCE_DIR = ROOT_DIR / "resource"
ROOT_CSV = RESOURCE_DIR / "root.csv"
COUNTER = RESOURCE_DIR / "counter.csv"
NT_FND_CNTR = RESOURCE_DIR / "not_found.csv"

# ENV
DOTENV_PATH = ROOT_DIR / ".env"
DRIVER_PATH = ROOT_DIR / "driver" / "chromedriver.exe"

# Output
OUTPUT_DIR = ROOT_DIR / "output"
if not OUTPUT_DIR.exists():
    Path.mkdir(OUTPUT_DIR)
TARGET_CSV = OUTPUT_DIR / "Updated_PNs_Equipments.csv"
TARGET_XLSX = OUTPUT_DIR / "Updated_PNs_Equipments.xlsx"

# Logs
LOG_DIR = ROOT_DIR / "log"
if not LOG_DIR.exists():
    Path.mkdir(LOG_DIR)
LOG_FILE = LOG_DIR / f"{TIME_NOW}.log"
