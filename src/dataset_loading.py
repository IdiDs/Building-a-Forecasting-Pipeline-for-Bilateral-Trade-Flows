from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "Data"

COUNTRY_PREFIXES = {
    "South Korea": "korea",
    "Slovakia": "slovakia",
    "USA": "usa",
}

SERIES_KEYS = ["Country1", "Country2", "ProductCode", "TradeFlow"]
TARGET = "Value"


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