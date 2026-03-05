import streamlit as st
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="Genetic CM: Final Financial Model", layout="wide")
st.title("🫀 Genetic Cardiomyopathy: Lifetime Economic Impact Model")
st.markdown("A modular tool to assess the financial gap between career earnings and heart failure interventions.")

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.header("1. Personal & Financial")
    age_diag = st.number_input("Age at Diagnosis (Screening)", value=20, min_value=1)
    max_age = st.slider("Retirement / Maximum Age", 40, 90, 60)
    salary = st.number_input("Starting Annual Salary (₹)", value=1200000)
    sal_growth = st.slider("Annual Salary Increment (%)", 0, 15, 6)
    med_inflation = st.slider("Annual Medical Inflation (%)", 0, 20, 12)
    
    st.header("2. Clinical Milestones")
    x_hf = st.slider("Age of Heart Failure Onset", age_diag + 1, max_age, 30)
    
    st.subheader("Surgical Modules & Timing")
    
    # ICD MODULE
    use_icd = st.checkbox("Include ICD Pathway", value=True)
    x_icd = 999
    if use_icd:
        x_icd = st.slider("Age at ICD Implant", age_diag, max_age, x_hf)

    # LVAD MODULE
    use_lvad = st.checkbox("Include LVAD Pathway", value=False)
    x_lvad = 999
    if use_lvad:
        x_lvad = st.slider("Age at LVAD Surgery", x_hf, max_age, 40)

    # TRANSPLANT MODULE
    use_htx = st.checkbox("Include Heart Transplant Pathway", value=False)
    x_ht = 999
    if use_htx:
        # Transplant can't happen before the latest of HF or LVAD
        min_ht_age = max(x_hf, x_lvad if use_lvad else 0)
        x_ht = st.slider("Age at Heart Transplant", min_ht_age, max_age, 50)
    
    st.header("3. Risk & ER Costs")
    hosp_prob = st.slider("Annual HF Hospitalization Risk (%)", 0, 100, 15)
    hosp_cost_base = st.number_input("Cost per Hospitalization (Current ₹)", value=200000, step=10000)

# --- COST DATABASE (2026 ESTIMATES) ---
COSTS = {
    "screening": 22000,      # Annual MRI/Echo/BB (Silent Phase)
    "gdmt": 94000,           # Annual HF Meds (Stage C)
    "icd_initial": 550000,   
    "icd_battery": 320000,   
    "lvad_initial": 8500000, 
    "lvad_maint": 50000,     # Annual kits/batteries
    "htx_initial": 2800000,  
    "htx_maint": 180000      # Annual Immunosuppressants
}

# --- CALCULATION ENGINE ---
ages = list(range(age_diag, max_age + 1))
income_curve, min_cost_curve, active_path_curve = [], [], []
cum_income, cum_min, cum_active = 0, 0, 0
curr_salary = salary
last_icd_age = 0 
peak_deficit = 0

for age in ages:
    y_idx = age - age_diag
    inf = (1 + med_inflation/100)**y_idx
    
    # 1. CUMULATIVE INCOME
    cum_income += curr_salary
    income_curve.append(cum_income)
    curr_salary *= (1 + sal_growth/100)
    
    # 2. BEST CASE (MINIMUM) - No symptoms, no failure
    annual_min = COSTS["screening"] * inf
    cum_min += annual_min
    min_cost_curve.append(cum_min)
    
    # 3. ACTIVE PATHWAY (CUSTOM MAX)
    annual_active = 0
    
    # --- PHASE: BEFORE TRANSPLANT ---
    if age < x_ht:
        # A. Medication Base
        if age < x_hf:
            annual_active = COSTS["screening"] * inf
        else:
            annual_active = COSTS["gdmt"] * inf
            # B. Hospitalization Risk (Only after HF onset)
            annual_active += (hosp_cost_base * (hosp_prob/100)) * inf
            
        # C. ICD Logic (Independent Age Trigger)
        if use_icd:
            if age == x_icd:
                annual_active += COSTS["icd_initial"] * inf
                last_icd_age = age
            elif last_icd_age > 0 and (age - last_icd_age) == 8:
                annual_active += COSTS["icd_battery"] * inf
                last_icd_age = age
                
        # D. LVAD Logic
        if use_lvad:
            if age == x_lvad:
                annual_active += COSTS["lvad_initial"] * inf
            elif age > x_lvad:
                annual_active += COSTS["lvad_maint"] * inf

    # --- PHASE: TRANSPLANT EVENT & AFTERMATH ---
    if use_htx and age == x_ht:
        annual_active += COSTS["htx_initial"] * inf
    elif use_htx and age > x_ht:
        # Everything stops except immunosuppressants and low complication risk
        annual_active = (COSTS["htx_maint"] + (hosp_cost_base * 0.05)) * inf

    cum_active += annual_active
    active_path_curve.append(cum_active)
    
    # Track "The Valley" (Max Deficit)
    current_gap = cum_active - cum_income
    if current_gap > peak_deficit:
        peak_deficit = current_gap

# --- VISUALIZATION ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=ages, y=income_curve, name="Total Career Earnings", fill='tozeroy', line=dict(color='#2ecc71', width=3)))
fig.add_trace(go.Scatter(x=ages, y=min_cost_curve, name="Best Case (Min Cost)", line=dict(color='#3498db', dash='dash')))
fig.add_trace(go.Scatter(x=ages, y=active_path_curve, name="Active Pathway Cost", line=dict(color='#e74c3c', width=4)))

fig.update_layout(title="Financial Sustainability Gap", xaxis_title="Age", yaxis_title="Rupees (₹)", hovermode="x unified", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# --- FINAL INSIGHTS ---
st.divider()
net_final = cum_income - cum_active
c1, c2, c3 = st.columns(3)
c1.metric("Final Earnings", f"₹{int(cum_income):,}")
c2.metric("Final Pathway Cost", f"₹{int(cum_active):,}")
c3.metric("Net Surplus/Deficit", f"₹{int(net_final):,}", delta=net_final)

if peak_deficit > 0:
    st.error(f"🛡️ **Peak Deficit Detected:** At your highest point of financial stress, you are short by ₹{int(peak_deficit):,}. This is the recommended **Insurance Cover** to stay solvent.")
else:
    st.success("✅ **Self-Sustaining:** Your projected earnings are sufficient for this pathway.")