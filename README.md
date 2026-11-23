# Building a Forecasting Pipeline for Bilateral Trade Flows

**Benchmarking Time Series and Machine Learning Models**  
Master's interdisciplinary Data Science project at TU Wien.

This project forecasts monthly bilateral trade flows for **South Korea, Slovakia and the USA**. Two complementary views compare forecasting methods: a six-model benchmark for **March 2026**, and a seven-model benchmark including Chronos-Bolt Tiny across three forecast origins and horizons of one to three months. Further experiments evaluate REER as an auxiliary data source and examine historical forecast behaviour around the March 2021 Suez Canal blockage. Numbered notebooks contain the research workflow, figures and interpretation.

## Research questions

| Question | Analysis |
|---|---|
| **RQ1:** How do machine learning models compare to classical time series approaches in forecasting trade flows? | March benchmark and repeated comparisons by origin, horizon, flow, HS chapter and size; notebooks 15–17 |
| **RQ2:** Do auxiliary data sources improve forecast accuracy? | Trade-only versus REER-enhanced XGBoost and LSTM; notebook 13 |
| **RQ3:** How do machine learning and classical time series models differ in their ability to capture and adapt to disruptive trade shocks? | ARIMA and XGBoost around the Suez blockage; notebook 14 |
| **RQ4:** What is the trade-off between model complexity and generalization performance? | Configuration choices, February-to-March performance, repeated accuracy and recorded evaluation-stage runtimes; notebooks 15–17 |

REER is the auxiliary source chosen for RQ2. The experiment does not evaluate auxiliary data sources generally.

## Project structure

```text
Data/
  raw/                         Original trade files and source documentation
  processed/                   Cleaned, harmonized trade datasets
  processed_monthly_complete/  Monthly panels with absent trade months set to zero
  features/                    Trade and calendar features
  forecasting/                 Training and March test datasets
  external_signals/            Downloaded BIS REER files
notebooks/                    Main workflow, notebooks 01–17
src/
  dataset_loading.py          Data loaders, series identifiers and saved notebook readers
  evaluation.py               Metrics and result-saving functions
results/                      March benchmarks and RQ1/RQ4 outputs
  reer/                       Auxiliary-signal comparison outputs
  suez/                       Historical shock-analysis outputs
  extended_benchmark/         Multi-origin forecasts, settings, metrics and figures
reports/                      Proposal and report material
requirements.txt              Python dependencies
README.md                     Project overview and reproduction guide
```

## Data

Trade sources are documented in notebooks 01–04: OEC for South Korea, Eurostat for Slovakia, and US Census Bureau state-level data for the USA, aggregated during preparation.

| Country | Harmonized historical coverage | March 2026 test series |
|---|---|---:|
| South Korea | January 2019–May 2026 | 27,823 |
| Slovakia | January 2015–March 2026 | 21,973 |
| USA | January 2017–April 2026 | 35,843 |

Each monthly series is identified by `Country1`, `Country2`, `ProductCode` and `TradeFlow`. The time index is `Month` and the target is `Value`.

**Absent monthly trade observations are assigned zero**, following the supervisor's instruction, without interpolation. Preparation applies history, partner/product coverage and zero-share filters, including exclusion of series with more than 90% zero months. The original cohort selection is retrospective; fitting the March models uses observations through February only.

Monthly real, broad-basket REER indices from BIS are stored under `Data/external_signals/` as `korea_bis_reer.csv`, `slovakia_bis_reer.csv` and `usa_bis_reer.csv`. Notebook 13 records source URLs and checks dates, frequency, missing values and country codes. A two-month reference lag means March uses January REER. Missing aligned REER values raise an error rather than being imputed.

Data files must be available locally; installing dependencies does not download them. Raw preprocessing is substantial, particularly the approximately 47 GB US source file.

## Setup

The project was run **with Python 3.11**. Navigate to your checkout before installing dependencies. Replace the example project path with your own.

**Windows (PowerShell):**

```powershell
Set-Location "C:\path\to\InterdisciplinaryProject"
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `.venv` already exists, use it without recreating it. Launch Jupyter from the notebook directory:

```powershell
cd notebooks
..\.venv\Scripts\python.exe -m jupyterlab
```

**Linux/macOS (Bash or Zsh):**

```bash
cd /path/to/InterdisciplinaryProject
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
cd notebooks
../.venv/bin/python -m jupyterlab
```

Select the project's `.venv` Python kernel and open notebooks from the Jupyter file browser. Launching Jupyter after `cd notebooks` gives early notebooks the working directory they expect: they locate the project root as its parent. Later notebooks accept either the project root or `notebooks/`. When using an editor such as VS Code, set the notebook kernel working directory to the notebook's folder (`notebooks/`). To check it, evaluate `Path.cwd()` after importing `Path` from `pathlib`; if needed, run `%cd /path/to/InterdisciplinaryProject/notebooks` in the kernel before processing cells.

Dataset paths consistently use `Data/`, matching the actual directory name on case-sensitive filesystems. Full Linux/macOS execution has not been tested; the commands above provide the equivalent setup and navigation.


## Notebook execution order

For a full reconstruction, follow this order and execute each notebook from top to bottom:

| Notebook | Purpose |
|---|---|
| [01 — Data inventory](notebooks/01_data_inventory.ipynb) | Inspect raw files, schemas and coverage |
| [02 — Korea preprocessing](notebooks/02_korea_preprocessing.ipynb) | Prepare South Korean trade data |
| [03 — Slovakia preprocessing](notebooks/03_slovakia_preprocessing.ipynb) | Prepare Slovak trade data |
| [04 — USA preprocessing](notebooks/04_usa_preprocessing.ipynb) | Clean and aggregate US state-level data |
| [05 — Cross-country validation](notebooks/05_cross_country_validation.ipynb) | Harmonize and check datasets; this is data validation, not model validation |
| [06 — Exploratory analysis](notebooks/06_exploratory_data_analysis.ipynb) | Explore trade patterns and construct completed monthly panels |
| [07 — Feature engineering](notebooks/07_feature_engineering.ipynb) | Select series and construct historical and calendar features |
| [08 — Forecasting preparation](notebooks/08_forecasting_preparation.ipynb) | Save history through February and held-out March observations |
| [09 — Baselines](notebooks/09_baseline_models.ipynb) | Evaluate Naive and Seasonal Naive |
| [10 — Statistical models](notebooks/10_statistical_models.ipynb) | Fit and evaluate ETS and ARIMA |
| [11 — XGBoost](notebooks/11_machine_learning_models.ipynb) | Select configurations on February, refit and predict March |
| [12 — LSTM](notebooks/12_deep_model.ipynb) | Select architectures and epochs on February, refit and predict March |
| [13 — External signals](notebooks/13_external_signal.ipynb) | Compare saved trade-only scores with fitted REER variants |
| [14 — Suez analysis](notebooks/14_suez_canal_analysis.ipynb) | Generate historical January–June 2021 forecasts and evaluate shock response |
| [15 — Model comparison](notebooks/15_model_comparison.ipynb) | Analyse saved benchmark and configuration results without training |
| [16 — Extended forecasting benchmark](notebooks/16_extended_forecasting_benchmark.ipynb) | Select direct configurations and forecast three origins and horizons, including Chronos |
| [17 — Extended results comparison](notebooks/17_extended_results_comparison.ipynb) | Compare saved forecasts by origin, horizon, HS chapter, flow and size without retraining |

**Save notebooks 11 and 12 with their displayed validation tables intact.** Notebooks 13 and 15 read those saved tables and configuration dictionaries; notebook 14 reads the XGBoost selection from notebook 11. Separate validation-result files are not required.

Notebooks 13, 14 and 16 reuse `read_notebook_setting` and, where needed, `read_validation_table` from `src/dataset_loading.py`. These readers inspect saved notebook content without executing it. Experiment-specific preparation and model code remain in the notebooks.

Reuse prepared data and completed results when available. Notebooks 01–12 do not need to be rerun just to read the findings. Notebook 15 can run directly when its benchmark CSVs, March target files and saved validation outputs are present. Notebook 13 refits the REER models; notebook 14 refits historical models on every fresh run. Result-saving cells replace their documented output files when rerun.

## Experimental design

- **Baselines:** Naive uses February's value; Seasonal Naive uses the previous March's value.
- **Statistical models:** additive-trend ETS without seasonality and fixed ARIMA(1,1,1) are fitted separately to individual series. Notebook 10 does not perform a configuration search.
- **XGBoost:** three predefined configurations are compared on February MAE, using fitting data through January. The selected country model is refitted through February to predict March. Predictors include lags 1, 2, 3, 6 and 12; shifted rolling means and standard deviations over 3, 6 and 12 months; and three calendar features.
- **LSTM:** three architectures are compared on February MAE. Each country has one shared model trained on twelve-month windows drawn separately from individual series. The target uses `log1p` and fitting-period standardization, with inverse transformation once. Epoch selection allows up to 15 epochs with patience 5; the final model is refitted for the selected duration.
- **Auxiliary data:** selected configurations and March targets are retained. REER is an additional XGBoost predictor and a scalar appended to the LSTM hidden output. REER LSTM selects its own epoch count using the same February procedure. Original trade-only scores are reused.
- **Suez analysis:** trade-only ARIMA and XGBoost use 200 high-value series per country, selected and frozen using December 2020 and earlier information. Models are refitted at six successive origins: January uses history through December, February through January, and so on. These are one-month-ahead forecasts, not a six-month forecast made before the event. Handled ARIMA fitting failures use a recorded Naive fallback to retain matched observations.

**sMAPE (%) is the primary reporting metric; February MAE selects machine learning configurations.** MAE, RMSE and evaluated series counts are also reported. Lower errors are better. Both-zero actual/forecast pairs contribute zero to sMAPE. REER changes are enhanced minus trade-only: negative values indicate improvement. sMAPE percentage-point differences are distinguished from relative percentage changes.

## Saved results

| Notebook | Location | Files |
|---|---|---|
| 09 | `results/` | `baseline_results.csv` |
| 10 | `results/` | `statistical_results.csv` (ETS), `arima_results.csv` |
| 11 | `results/` | `xgboost_results.csv` |
| 12 | `results/` | `lstm_results.csv` |
| 13 | `results/reer/` | `reer_comparison.csv`, `model_comparison.png`, `metric_changes_heatmap.png` |
| 14 | `results/suez/` | `monthly_results.csv`, `period_results.csv`, `actual_vs_forecast.png`, `monthly_errors.png` |
| 15 | `results/` | `rq1_benchmark_results.csv`, `rq1_smape_comparison.png`, `rq1_metric_rankings.png`, `rq4_configuration_results.csv`, `rq4_configuration_performance.png`, `rq4_validation_test_comparison.csv`, `rq4_validation_test_mae.png` |

Benchmark CSVs contain aggregate metrics, not individual forecasts. REER and Suez predictions remain in notebook memory rather than separate prediction files. Suez period scores pool series-month errors: 400 observations before the event, 200 in March and 600 after it per country and model. Pooled RMSE combines squared errors before taking the square root.

## Extended benchmark

Run **16, then 17** for the additional experiment. The existing March, REER and Suez outputs remain separate. Notebook 16 reads `Data/processed/` and the candidate dictionaries in notebooks 11 and 12; it performs its own configuration selection rather than reusing their March choices.

| History through | Horizon 1 | Horizon 2 | Horizon 3 |
|---|---|---|---|
| April 2025 | May 2025 | June 2025 | July 2025 |
| August 2025 | September 2025 | October 2025 | November 2025 |
| December 2025 | January 2026 | February 2026 | March 2026 |

Cohort eligibility, partner selection and size terciles use December 2024 and earlier information. The series, HS chapter prefixes, flows and size classes stay fixed. Missing months remain zero, including later inactivity; no series cap is applied. Tied pre-cutoff trade values stay in the same size class, so terciles can have unequal counts.

Configurations are selected separately by country and horizon: fit through December 2024 and validate January, February or March 2025 for horizons 1, 2 or 3. Separate direct XGBoost and LSTM models are refitted at each origin. Every LSTM refit selects new epochs using an internal chronological holdout, then refits on the full available history. ETS and ARIMA retain notebook 10's fixed specifications, with recorded Naive fallbacks keeping failed historical fits in the extended comparison.

Chronos-Bolt Tiny uses a pinned November-2024 revision and median forecasts, without fine-tuning. The checkpoint predates evaluation, while overlap with older trade histories in pretraining is unverified. The first load downloads public weights to the standard Hugging Face cache. Dependencies are included in `requirements.txt`; existing PyTorch/device selection is retained.

All extension outputs are saved under `results/extended_benchmark/`:

| File | Contents |
|---|---|
| `predictions.parquet` | Keys, country, model, origin, horizon, target month, actual, forecast, frozen groups, source flags and fallback reasons |
| `model_settings.csv` | Configurations, fresh LSTM epochs and validation dates, device, runtime, fallback counts and pinned checkpoint revision |
| `origin_metrics.csv` | MAE, RMSE, sMAPE and comparison to Naive for each country, model, origin and horizon |
| `group_metrics.csv` | The same origin-specific comparisons within HS chapters, imports/exports and size classes |
| `accuracy_by_horizon.png` | Country-origin panels comparing horizons 1–3 |
| `accuracy_by_origin.png` | Country-horizon panels comparing the three origins |
| `relative_accuracy_by_{hs,flow,size}_{country}_{origin}.png` | Separate country-origin group figures, each with three horizon panels |

Relative improvement is `100 × (Naive error − model error) / Naive error`: positive is better. Zero reference error gives an undefined relative change. Groups below 30 series are flagged but retained. Primary results are not pooled across origins. There are 27 detailed group figures plus the two overall figures.

Notebook 16 streams a partial Parquet file and publishes final outputs only when all models complete. Notebook 17 requires final predictions and settings from the same run and checks complete keys and actuals against Naive. Partial files are not accepted. Validation records stay in notebook displays; no model weights or additional feature datasets are saved.

## Main findings

- **RQ1:** Naive has the lowest March sMAPE for South Korea (74.62%); ARIMA leads Slovakia (70.26%) and the USA (72.32%). Neither XGBoost nor LSTM beats the best classical sMAPE within a country. Rankings depend on the metric: US ARIMA has the best sMAPE but the worst RMSE, while ETS leads US MAE and RMSE. In the complementary multi-origin view, Naive leads overall sMAPE in 26 of 27 country-origin-horizon comparisons, while Chronos leads MAE in 23. Subgroup results reveal useful differences: Chronos leads large-flow Korean and medium/large-flow US sMAPE in all nine comparisons for each group, and consistently improves on Naive for selected US product chapters.
- **RQ2:** Auxiliary data offer conditional benefits. USA REER LSTM reduces MAE by 14.78% and RMSE by 19.44%, with a 0.829 percentage-point sMAPE improvement. Both Slovak models and South Korean LSTM worsen throughout; the remaining XGBoost comparisons are mixed.
- **RQ3:** ARIMA has lower pooled post-event sMAPE and MAE in all three historical cohorts, while USA XGBoost has lower post-event RMSE. Both procedures respond to updated observations, but neither demonstrates advance event prediction or a causal Suez effect.
- **RQ4:** Greater capacity does not consistently improve validation accuracy. Selected configurations differ by country, and five of six selected machine learning pipelines have higher March MAE than February MAE. This temporal change alone does not establish overfitting. The extended experiment also shows that greater training effort does not ensure better accuracy: recorded evaluation-stage CPU time totals approximately 5.1 minutes for Chronos inference versus 14.88 hours for LSTM epoch selection, refits and predictions. Initial configuration search and Chronos pretraining are excluded, so these are partial workflow timings rather than total development costs.

Detailed interpretation of the March, REER and Suez findings appears at the ends of notebooks 13–15. Notebook 17 presents the extended results by origin, horizon and trade group; the report brings both forecasting views together.

## Assumptions and limitations

The original March experiment uses one February holdout, small configuration grids and reuse of completed benchmarks. Its cohort selection is retrospective, and saved original predictions are unavailable for an independent paired audit. The complementary extension freezes cohorts using December 2024 and earlier information and evaluates three spaced origins and three horizons. This broadens the evidence but remains a limited set of dates rather than proof of general performance across time.

Zero completion assumes absent records mean no trade. Preceding-month trade availability is assumed; revised REER snapshots and the two-month lag do not guarantee historical publication availability. Raw MAE and RMSE are compared within countries rather than averaged across source scales.

The Suez analysis uses a high-value sample, a short window and XGBoost configurations selected with 2026 evidence. Historical fitting is chronological, but configuration selection is retrospective. Verified shipping-route exposure, controls and publication vintages are unavailable, and changing source coverage may affect errors. Findings concern forecast response around the event, not causal attribution or general shock adaptation.

The original experiments did not systematically record runtime or memory. The extension records evaluation-stage elapsed times, including fresh LSTM epoch selection, while excluding initial configuration search, Chronos pretraining and some preparation. These support a qualified discussion of computational effort, not a complete or hardware-normalised efficiency benchmark; memory use was not systematically measured.
