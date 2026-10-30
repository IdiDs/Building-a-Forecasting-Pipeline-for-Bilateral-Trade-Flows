
from pathlib import Path

import numpy as np
import pandas as pd


RESULT_COLUMNS = [
    "Country",
    "Model",
    "Forecast Month",
    "N Series",
    "MAE",
    "RMSE",
    "sMAPE (%)",
]

# Resolve the project root from this file's location.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"


def evaluate_forecasts(
    country: str,
    model_name: str,
    actual,
    predicted,
    forecast_month: str = "2026-03",
) -> dict:
    """Evaluate forecasts using consistent metrics."""

    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    if actual.ndim != 1 or predicted.ndim != 1:
        raise ValueError("Actual and predicted values must be one-dimensional.")

    if len(actual) == 0:
        raise ValueError("Cannot evaluate an empty set of forecasts.")

    if len(actual) != len(predicted):
        raise ValueError(
            "Actual and predicted arrays must have the same length."
        )

    if not np.isfinite(actual).all():
        raise ValueError("Actual values contain NaN or infinite values.")

    if not np.isfinite(predicted).all():
        raise ValueError("Predictions contain NaN or infinite values.")

    absolute_error = np.abs(actual - predicted)

    mae = absolute_error.mean()
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))

    denominator = np.abs(actual) + np.abs(predicted)

    smape_terms = np.divide(
        2.0 * absolute_error,
        denominator,
        out=np.zeros_like(absolute_error),
        where=denominator != 0,
    )

    return {
        "Country": country,
        "Model": model_name,
        "Forecast Month": forecast_month,
        "N Series": len(actual),
        "MAE": float(mae),
        "RMSE": float(rmse),
        "sMAPE (%)": float(smape_terms.mean() * 100),
    }


def create_results_table(results: list[dict]) -> pd.DataFrame:
    """Create a consistently structured results table."""

    table = pd.DataFrame(results, columns=RESULT_COLUMNS)

    if not table.empty:
        table = table.sort_values(
            ["Country", "MAE"],
            ignore_index=True,
        )

    return table


def save_model_results(
    results: list[dict],
    model_name: str,
) -> pd.DataFrame:
    """Save a separate CSV results table for one model."""

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(
        char.lower() if char.isalnum() else "_"
        for char in model_name
    ).strip("_")

    output_path = RESULTS_DIR / f"{safe_name}_results.csv"
    results_table = create_results_table(results)
    results_table.to_csv(output_path, index=False)

    print(f"Saved model results to: {output_path}")

    return results_table


def append_results(
    existing_results: pd.DataFrame,
    new_results: list[dict],
) -> pd.DataFrame:
    """Append new evaluation results to an existing table in memory."""

    if not set(RESULT_COLUMNS).issubset(existing_results.columns):
        raise ValueError(
            "Existing results table does not contain all required columns."
        )

    new_table = create_results_table(new_results)

    combined = pd.concat(
        [existing_results[RESULT_COLUMNS], new_table],
        ignore_index=True,
    )

    return combined.sort_values(
        ["Country", "MAE"],
        ignore_index=True,
    )


def combine_model_results() -> pd.DataFrame:
    """Combine individual model result CSVs and save the common table."""

    if not RESULTS_DIR.exists():
        raise FileNotFoundError(
            f"Results directory does not exist: {RESULTS_DIR}"
        )

    result_files = sorted(
        path
        for path in RESULTS_DIR.glob("*_results.csv")
        if path.name != "all_model_results.csv"
    )

    if not result_files:
        raise FileNotFoundError(
            f"No individual model result files found in {RESULTS_DIR}."
        )

    tables = []

    for path in result_files:
        table = pd.read_csv(path)

        missing_columns = set(RESULT_COLUMNS) - set(table.columns)
        if missing_columns:
            raise ValueError(
                f"{path.name} is missing columns: {sorted(missing_columns)}"
            )

        tables.append(table[RESULT_COLUMNS])

    combined = pd.concat(tables, ignore_index=True)
    combined = combined.sort_values(
        ["Country", "MAE"],
        ignore_index=True,
    )

    output_path = RESULTS_DIR / "all_model_results.csv"
    combined.to_csv(output_path, index=False)

    print(f"Saved combined results to: {output_path}")

    return combined

