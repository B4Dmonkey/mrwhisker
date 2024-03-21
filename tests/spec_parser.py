import yaml
from pytest import param
from pathlib import Path


def parse(file: str) -> list:
  file_path = Path(__file__).parent.parent/ "specs" / file 
  with open(file_path, "r") as f:
    for data in yaml.safe_load(f).get("tests"):
      name = data.pop("name")
      yield param(data, id=name)
