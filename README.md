# Cardiomyopathy_economical_model
A cost analysis tool for incidentally detected cardiomyopathy patients, based on their current salary, inflation rates etc. 



# 🫀 Genetic Cardiomyopathy: Lifetime Economic Impact Model (2026)

This interactive tool models the "Financial Fragility" of a life lived with a genetic heart condition. It compares **Cumulative Career Earnings** against a modular medical pathway.

### 📋 Assumption Database (India 2026 Projections)
The following base costs are used before applying annual medical inflation:

| Phase / Intervention | Estimated Base Cost (₹) | Frequency / Logic |
| :--- | :--- | :--- |
| **Annual Screening** | 22,000 | MRI, Echo, Beta-blockers (Silent Phase) |
| **Annual HF Meds (GDMT)** | 94,000 | ARNI, SGLT2i, etc. (After HF Diagnosis) |
| **Hospitalization** | User Defined | Statistical risk applied only after $x_{hf}$ |
| **ICD Implant** | 5,50,000 | Dual-chamber ICD + surgical fees |
| **ICD Battery** | 3,20,000 | Every 8 years (Stops after Transplant) |
| **LVAD Package** | 85,00,000 | HeartMate 3 + Surgery (Stops after Transplant) |
| **Heart Transplant** | 28,00,000 | Surgery + 1st Year ICU management |
| **Post-HTx Maintenance** | 1,80,000 / yr | Lifelong Immunosuppressants |

---

### 🧮 Calculation Formulas

**1. Cumulative Income** (Growth rate $g$):
$$Total\ Income = \sum_{t=diag}^{max} \text{Salary}_0 \times (1 + g)^{(t - diag)}$$

**2. Inflation-Adjusted Costs** (Medical inflation $m$):
$$Cost_{future} = Cost_{base} \times (1 + m)^{(t - diag)}$$

**3. Annual Hospitalization Risk** (Expected Value):
$$E = (\text{Cost per Hosp.} \times \text{Prob \%}) \times (1 + m)^{year}$$

**4. Peak Deficit (The Insurance Gap):**
The model identifies the specific age where the medical debt is highest relative to savings:
$$\text{Gap} = \max( \text{Cumulative Costs}_t - \text{Cumulative Income}_t )$$



---

### 📌 Clinical Logic & Triggers
- **Phase 1 (Silent):** Annual screening costs only.
- **Phase 2 (Heart Failure $x_{hf}$):** Medication costs jump. Hospitalization risk activates.
- **Phase 3 (Mechanical Bridge):** LVAD costs + maintenance kits start.
- **Phase 4 (Transplant $x_{ht}$):** Final "Pivot." Stops ICD/LVAD costs and HF risk; starts Post-HTx immunosuppressant protocol.



---

### 🚀 Deployment Guide
1. Create a GitHub repo.
2. Upload `app.py` and `requirements.txt` (containing `streamlit` and `plotly`).
3. Connect to **Streamlit Cloud** and deploy.

*Disclaimer: This is a financial simulation tool for planning purposes and does not constitute medical or financial advice.*
