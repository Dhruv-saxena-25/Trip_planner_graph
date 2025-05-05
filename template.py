import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

# List all files (and their parent dirs) you want to ensure exist.
list_of_files = [
    ".env",
    "app.py",
    "requirements.txt",
    "template.py",
    ".github/workflows/main.yml",
    "src/__init__.py",
    "src/graph/__init__.py",
    "src/graph/built_graph.py",
    "src/llms/__init__.py",
    "src/llms/llms.py",
    "src/mail/__init__.py",
    "src/mail/email.py",
    "src/tools/__init__.py",
    "src/tools/city.py",
    "src/tools/flight.py",
    "src/tools/hotel.py",
    "src/tools/weather.py",
    "src/state/__init__.py",
    "src/state/custom_state.py",
    "src/planner/__init__.py",
    "src/planner/plan.py",
]

for filepath_str in list_of_files:
    filepath = Path(filepath_str)
    filedir = filepath.parent
    filename = filepath.name

    # create parent directories if needed
    if filedir != Path():
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    # create the file if it doesn't exist or is empty
    if (not filepath.exists()) or (filepath.stat().st_size == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
