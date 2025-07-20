import yaml
from typing import Any

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def get_project_names() -> list[str]:
    return [p["name"] for p in config["projects"]]

def get_project_by_name(project_name: str) -> dict[str, Any] | None:
    return next((p for p in config["projects"] if p["name"] == project_name), None)