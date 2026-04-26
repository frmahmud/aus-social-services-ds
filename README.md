# Social Services Demand Risk Predictor 🇦🇺

> **End-to-end data science project — Australian Public Sector**  
> Predicting welfare demand risk across SA2 regions using open government data.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Data](https://img.shields.io/badge/Data-Open%20Government-orange)](https://data.gov.au)

---

## Project Overview

The Australian Department of Social Services (DSS) supports millions of 
Australians through welfare payments and community services. This project 
asks: **can we proactively identify which communities face the highest 
risk of increased welfare demand?**

Using entirely free, publicly available data from ABS, DSS, and AIHW, 
this project delivers three analytical outputs:

| Task | Technique | Result |
|---|---|---|
| Risk classification | XGBoost + scikit-learn | F1 macro = 0.000 |
| Demand forecasting | Prophet + ARIMA | 4-quarter ahead forecast |
| Policy text analysis | LDA + VADER sentiment | 6 topics tracked 2018–2023 |

---

## Key Finding

High-risk SA2 regions are concentrated in:
- **Northern Territory** — remote communities with high SEIFA disadvantage
- **Remote Western Australia and South Australia** — low IRSD decile regions  
- **Outer suburban corridors** of major cities — population growth + service gaps

SHAP analysis confirmed that **IRSD score** is the single most important 
predictive feature, followed by remoteness classification and population size.

---

## Repository Structure

```
aus-social-services-ds/
│
├── notebooks/
│   ├── 01_problem_framing.ipynb        # Problem statement, data strategy, ethics
│   ├── 02_data_collection.ipynb        # ABS/DSS data ingestion pipelines
│   ├── 03_eda.ipynb                    # Exploratory data analysis (15+ charts)
│   ├── 04_feature_engineering.ipynb    # Feature engineering + preprocessing pipeline
│   ├── 05_modelling.ipynb              # LR → RF → XGBoost + Prophet forecasting
│   ├── 06_nlp_policy_analysis.ipynb    # LDA topic model + VADER sentiment
│   └── 07_executive_report.ipynb       # This notebook — reporting & deployment
│
├── data/
│   ├── raw/          # Source files (not tracked in Git)
│   └── processed/    # Cleaned, feature-engineered outputs
│
├── models/           # Serialised model files (not tracked in Git)
├── app/
│   └── dashboard.py  # Plotly Dash interactive dashboard
├── reports/          # Charts and HTML exports
├── MODEL_CARD.md     # Model documentation and limitations
├── requirements.txt  # Python dependencies
└── README.md
```

---

## Setup & Run

### Prerequisites
- Python 3.11+
- Windows / macOS / Linux
- ~2 GB disk space for datasets

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/aus-social-services-ds.git
cd aus-social-services-ds

# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Launch JupyterLab
jupyter lab
```

### Run notebooks in order
Open each notebook in `notebooks/` and run **Run → Run All Cells**:

```
01 → 02 → 03 → 04 → 05 → 06 → 07
```

### Launch the dashboard

```bash
python app/dashboard.py
# Open http://127.0.0.1:8050
```

---

## Data Sources

All data is open, publicly available, and licensed under CC BY 4.0:

| Dataset | Source | URL |
|---|---|---|
| ABS SEIFA 2021 | Australian Bureau of Statistics | [abs.gov.au](https://abs.gov.au) |
| DSS Payment Data | Department of Social Services | [data.gov.au](https://data.gov.au) |
| Regional Population | Australian Bureau of Statistics | [abs.gov.au](https://abs.gov.au) |
| DSS Annual Reports | Department of Social Services | [dss.gov.au](https://dss.gov.au) |

---

## Ethics & Limitations

This project uses only **aggregated, non-personal data** at SA2 region level.
No individual-level data was accessed or used.

See [MODEL_CARD.md](MODEL_CARD.md) for full documentation of model limitations,
ethical considerations, and recommendations for responsible use.

---

## Author

**Firoz Mahmud**  
fmahmud.ruet@gmail.com
Data Analyst
Department of Social Services  

---

## Licence

MIT Licence — see [LICENSE](LICENSE) for details.  
Data sources: CC BY 4.0 (Australian Government Open Data)
