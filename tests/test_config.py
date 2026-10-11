
from pathlib import Path

import yaml


CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.yaml"


def test_config_has_required_sections():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    assert "project" in config
    assert "macro_calendar" in config
    assert "data" in config
    assert "validation" in config


def test_macro_calendar_settings_are_valid():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    calendar = config["macro_calendar"]

    assert calendar["impact_min"] in {"Low", "Medium", "High"}
    assert 1 <= calendar["max_results_per_run"] <= 10
    assert isinstance(calendar["countries"], list)
