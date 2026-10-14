import os

from dotenv import load_dotenv
from rich import print
from rich.markdown import Markdown

load_dotenv()

greetings = os.getenv("GREETINGS", "`.env` file not found, check `.env-example`")

print(Markdown("---"))
print(greetings)
print(Markdown("---"))
