from pathlib import Path
import ast
import json

import pandas as pd
from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "Data"

COUNTRY_PREFIXES = {
    "South Korea": "korea",
    "Slovakia": "slovakia",
    "USA": "usa",
}

SERIES_KEYS = ["Country1", "Country2", "ProductCode", "TradeFlow"]
TARGET = "Value"


def read_notebook_setting(notebook_name, variable_name):
    """Read a literal setting without executing the source notebook."""
    path = PROJECT_ROOT / "notebooks" / notebook_name
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        for node in ast.walk(ast.parse("".join(cell["source"]))):
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == variable_name
                for target in node.targets
            ):
                return ast.literal_eval(node.value)
    raise ValueError(f"{variable_name} was not found in {notebook_name}.")


def read_validation_table(notebook_name, required_columns):
    """Read a displayed validation table saved with a completed notebook."""
    path = PROJECT_ROOT / "notebooks" / notebook_name
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for cell in notebook["cells"]:
        for output in cell.get("outputs", []):
            html = "".join(output.get("data", {}).get("text/html", []))
            for table in BeautifulSoup(html, "html.parser").find_all("table"):
                columns = [item.get_text(strip=True) for item in table.select("thead th")]
                columns = [name for name in columns if name]
                if not set(required_columns).issubset(columns):
                    continue
                rows = [
                    [item.get_text(strip=True) for item in row.find_all("td")]
                    for row in table.select("tbody tr")
                ]
                return pd.DataFrame(rows, columns=columns)
    raise ValueError(
        f"Save {notebook_name} with its validation table outputs first. "
        "No configuration is selected from test results."
    )


def load_forecasting_data(countries=None):
    """Load training and test datasets for the selected countries."""
    if countries is None:
        countries = list(COUNTRY_PREFIXES.keys())

    forecast_dir = DATA_DIR / "forecasting"
    training_data = {}
    test_data = {}

    for country in countries:
        if country not in COUNTRY_PREFIXES:
            raise ValueError(f"Unknown country: {country}")

        prefix = COUNTRY_PREFIXES[country]

        train_path = forecast_dir / f"{prefix}_train.parquet"
        test_path = forecast_dir / f"{prefix}_test.parquet"

        training_data[country] = pd.read_parquet(train_path)
        test_data[country] = pd.read_parquet(test_path)

        training_data[country]["Month"] = pd.to_datetime(
            training_data[country]["Month"]
        )
        test_data[country]["Month"] = pd.to_datetime(
            test_data[country]["Month"]
        )

    return training_data, test_data


def load_feature_data(countries=None):
    """Load feature-engineered datasets for the selected countries."""
    if countries is None:
        countries = list(COUNTRY_PREFIXES.keys())

    feature_dir = DATA_DIR / "features"
    feature_data = {}

    for country in countries:
        if country not in COUNTRY_PREFIXES:
            raise ValueError(f"Unknown country: {country}")

        prefix = COUNTRY_PREFIXES[country]
        path = feature_dir / f"{prefix}_trade_features.parquet"

        feature_data[country] = pd.read_parquet(path)
        feature_data[country]["Month"] = pd.to_datetime(
            feature_data[country]["Month"]
        )

    return feature_data
