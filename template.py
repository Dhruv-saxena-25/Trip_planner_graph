import os

dirs = [
    ".venv",
    "src",
    "src/graph",
    "src/llms",
    "src/mail",
    "src/tools",
    "src/state",
    "src/planner",
]

files = {
    ".env": "",
    "app.py": "",
    "requirements.txt": "",
    "src/__init__.py": "",
    "src/graph/__init__.py": "",
    "src/graph/built_graph.py": "",
    "src/llms/__init__.py": "",
    "src/llms/llms.py": "",
    "src/mail/__init__.py": "",
    "src/mail/email.py": "",
    "src/tools/__init__.py": "",
    "src/tools/city.py": "",
    "src/tools/flight.py": "",
    "src/tools/hotel.py": "",
    "src/tools/weather.py": "",
    "src/state/__init__.py": "",
    "src/state/custom_state.py": "",
    "src/planner/__init__.py": "",
    "src/planner/plan.py": "",
}

def create_structure():
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    for path, content in files.items():
        parent = os.path.dirname(path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    create_structure()
    print("Scaffold complete")
