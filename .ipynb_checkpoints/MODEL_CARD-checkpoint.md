# Model Card — Social Services Demand Risk Predictor

**Model name:** Welfare Demand Risk Classifier  
**Model type:** Multi-class classification  
**Version:** 1.0  
**Date:** 26 April 2026  
**Author:** [Your Name]  
**Repository:** aus-social-services-ds  

---

## Model Description

This model classifies Australian Statistical Area Level 2 (SA2) regions 
into three welfare demand risk tiers — High, Medium, and Low — based on 
socioeconomic, geographic, and demographic features derived from publicly 
available ABS and DSS data.

It is intended as a **research and portfolio tool** to demonstrate 
end-to-end data science applied to Australian public sector problems. 
It is not intended for operational use in welfare decision-making.

---

## Intended Use

### Intended uses
- Portfolio demonstration of end-to-end DS methodology
- Research into geographic patterns of welfare demand
- Educational example of responsible ML in government contexts
- Starting point for further analysis with richer longitudinal data

### Out-of-scope uses
- Direct allocation or denial of welfare payments to individuals
- Automated eligibility assessments
- Profiling of individual citizens
- Any use that treats model output as ground truth without expert review

---

## Training Data

| Dataset | Source | Version | Licence |
|---|---|---|---|
| ABS SEIFA 2021 (SA2) | Australian Bureau of Statistics | 2021 Census | CC BY 4.0 |
| DSS Payment Demographic Data | Department of Social Services | Jun 2023 | CC BY 4.0 |
| ABS Regional Population | Australian Bureau of Statistics | 2021-22 | CC BY 4.0 |

**No individual-level data was used.** All data is aggregated at SA2 
region level (3,000–25,000 residents per region).

---

## Model Performance

| Metric | Value | Target | Met? |
|---|---|---|---|
| F1 Score (macro) | 0.000 | ≥ 0.70 | ✗ |
| F1 Score (weighted) | See report | ≥ 0.70 | — |
| ROC-AUC (macro OVR) | See report | ≥ 0.80 | — |

Evaluation was performed on a held-out test set (15% of data) 
that was not used during training or hyperparameter tuning.

---

## Features Used

| Feature | Description | Source |
|---|---|---|
| irsd_score | Index of Relative Socio-economic Disadvantage | ABS SEIFA |
| irsad_score | Index of Relative Socio-economic Advantage & Disadvantage | ABS SEIFA |
| irsd_decile | IRSD decile (1–10, 1 = most disadvantaged) | ABS SEIFA |
| log_population | Log-transformed usual resident population | ABS SEIFA |
| score_range | Difference between IRSAD and IRSD scores | Engineered |
| disadvantage_flag | Binary: 1 if IRSD decile ≤ 3 | Engineered |
| remoteness_encoded | Urban=0, Regional=1, Remote=2 | Engineered |
| state_encoded | Ordinal encoding of state/territory | ABS SEIFA |

---

## Limitations & Risks

### Known limitations
1. **Cross-sectional only** — trained on a single point in time. 
   Does not capture within-region change dynamics over time.

2. **Geographic aggregation** — SA2 regions mask significant 
   intra-region variation. High-risk individuals may live in 
   Low-risk regions and vice versa.

3. **Feature proxies** — remoteness and state are imperfect proxies 
   for the complex social factors driving welfare demand.

4. **Class imbalance** — the model was trained with SMOTE oversampling 
   and balanced class weights. Performance on the minority (High-risk) 
   class may be lower in deployment on new data.

### Ethical considerations
1. **Stigmatisation risk** — labelling communities as "High risk" 
   could be misused to stigmatise regions rather than to direct support.
   The model output should always be framed as "likely to benefit from 
   additional support", not "likely to be a burden".

2. **Indigenous communities** — a disproportionate share of High-risk 
   regions are in remote areas with significant Indigenous populations. 
   Any use of this model in Indigenous policy contexts must involve 
   consultation with affected communities and Indigenous data governance 
   frameworks (AIATSIS Code of Ethics).

3. **Self-fulfilling prophecy** — if resource allocation follows model 
   predictions, regions predicted as Low-risk may receive less support, 
   which could cause their situation to deteriorate — a feedback loop 
   that the model cannot detect.

---

## Recommendations for Safe Use

- Always combine model outputs with local knowledge and qualitative context
- Treat predictions as one input among many, not as a decision
- Re-train annually as new DSS payment data and ABS updates become available
- Commission an independent bias audit before any operational deployment
- Establish a human review process for any High-risk classification that 
  informs a policy decision

---

## Caveats

This model was developed as a **portfolio project** using open data. 
The author is not responsible for any decisions made using its outputs. 
The model has not undergone external validation or independent audit.

---

*Model card template inspired by Mitchell et al. (2019) and the 
Australian Government AI Ethics Framework (2024).*
