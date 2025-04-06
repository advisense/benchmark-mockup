# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data

st.set_page_config(
    page_title="Cybersecurity Benchmark Dashboard mock-up",
    page_icon=":guardsman:",
    layout="wide",
)

industry_firms = {
    "Finance": [
        "Novabank", "EuroTrust Capital", "Altura Investments", "Helix Financial", "Zenith Bank Corp",
        "Quantis Holdings", "Arcadia Wealth", "Finexia Partners", "BluePeak Bank", "Lunaris Finance",
        "Stellar Credit", "Northern Crown Bank", "Meridian Capital", "Aureus Financial", "Cobalt Trust",
        "Ironridge Investments", "Pinnacle Banking", "Horizon Equity", "NovaCrest Finance", "TrustEdge Bank"
    ],
    "Healthcare": [
        "Mednova Clinics", "Vitalis Group", "CareBridge Health", "BioCure Systems", "Horizon Medical",
        "NeuraMedix", "PrimePath Health", "TheraLife Institute", "CureLine Biotech", "Veritas Care",
        "Wellspire Hospitals", "Lumena Clinics", "Nucleus Medical", "Evertrust Health", "Symmetry BioHealth",
        "MediCore Alliance", "Orion Healthworks", "Arbor Medical", "Helixia Therapeutics", "PulseBridge Group"
    ],
    "Manufacturing": [
        "CoreMach Industries", "FerroTech Solutions", "NexaFabrication", "OmniPlant Group", "Atlas Robotics",
        "MechWave Systems", "IronVale Manufacturing", "TitanAxis Engineering", "QuantumFoundry", "SteelRoot Works",
        "Nordic Assembly", "ArgoMech", "Constructix", "ForgeNova Group", "MetroSteel Fabricators",
        "LaminaTech", "Vertex Materials", "Kinetix Manufacturing", "MachOne Corp", "DeltaForge Systems"
    ],
    "Retail": [
        "ShopSphere", "Cartology", "UrbanCart", "Nordivo Retail", "Merco Online",
        "SwiftMart", "BrightBazaar", "NextBuy Group", "Orchid Retail", "Trendia Market",
        "LoopLane", "Clickaroo", "VeloShop", "RetailNova", "MaxCart Systems",
        "OptiCommerce", "StreamBuy", "Shelfie", "MarketPulse", "Groovix Retail"
    ],
    "Technology": [
        "NeuroNet Labs", "Opticore Systems", "ZenithSoft", "ByteRiver", "NovaNode",
        "AetherDigital", "Codexa Technologies", "NimbleStack", "DeepArc", "Cloudial",
        "Glideware", "SignalForge", "Tesseract Systems", "QuantumLayers", "Infrabyte Group",
        "TriloTech", "EchoNetics", "CoreNova AI", "BrightBridge", "SyntraLogic"
    ],
    "Energy": [
        "VoltEdge Energy", "GridCore Solutions", "Solara Utilities", "HydroPulse", "Elexa Energy",
        "TerraVolt", "ZenPower Corp", "LumeraGrid", "FusionField Energy", "PowerHive",
        "EcoGenix", "BrightFlow Energy", "AmpEdge Utilities", "ClearGrid Systems", "Hydrion Energy",
        "Solarithm", "TidalCore", "VoltraGrid", "NextCurrent", "BlueWatt Energy"
    ],
    "Automotive": [
        "Velomotive", "Axelra Motors", "TritonDrive", "Quantum AutoWorks", "Nexora Mobility",
        "AutoNova Group", "StratosDrive", "OmniTorque", "FusionDrive Systems", "Orbis Motors",
        "Mechaneer Auto", "Roadstride Corp", "Motivara Engineering", "Ignitia Automotive", "CruxDrive",
        "Voltic Motors", "IronAxis Vehicles", "BlueLine Auto", "Gravix Motors", "ZenithDrive"
    ],
    "Public Sector": [
        "Nordic Municipal Authority", "Central Public Works", "StateTech Administration", "Urban Services Office",
        "Metro Infrastructure Council", "E-Government Bureau", "National Digital Directorate", "GreenPolicy Agency",
        "Ministry of Civil Infrastructure", "Department of Innovation Services", "Urban Development Council",
        "Public Resource Network", "National Cyber Unit", "Transport Modernization Office", "Energy Regulation Board",
        "Digital Cities Program", "Government Data Systems", "Public Finance Agency", "SecureGov IT", "CivicTech Council"
    ],
    "Aerospace & Defense": [
        "Skyris Defense", "OrbitalEdge Aerospace", "Aviatrix Systems", "Novastra Dynamics", "Vectorion Technologies",
        "Skyfront Defense", "StellarAero", "Graviton Defense Group", "ThrustCore Systems", "QuantumFlight Labs",
        "Aerodyne Command", "Helion Defense", "IonGuard Aerospace", "FalconNova Industries", "Sentron Systems",
        "Cosmaero Group", "LaunchPath Defense", "Vortexa Aerospace", "IgnitionPoint Tech", "AstroDynamics Corp"
    ]
}



# ------------------
# Generate mock data
# ------------------
np.random.seed(42)
industries = list(industry_firms.keys())
functions = ['Identify', 'Protect', 'Detect', 'Respond', 'Recover']
subcategories = [f"{func}.{i}" for func in functions for i in range(1, 6)]

@st.cache_data
def generate_mock_data():
    np.random.seed(42)

    data = []
    for industry in industries:
        firm_names = industry_firms[industry]
        for firm in firm_names:
            spend_percent = np.clip(np.random.normal(7, 2), 2, 15)
            base_maturity = np.clip(0.5 * spend_percent + np.random.normal(0, 1), 1, 5)

            maturity_scores = np.clip(
                np.random.normal(base_maturity, 0.5, len(functions)),
                1, 5
            )
            total_maturity = np.mean(maturity_scores)

            sub_scores = np.clip(
                np.random.normal(base_maturity, 0.6, len(subcategories)),
                1, 5
            )

            data.append({
                "Organization": firm,
                "Industry": industry,
                "Spend (%)": spend_percent,
                "Maturity": total_maturity,
                **{func: score for func, score in zip(functions, maturity_scores)},
                **{sub: score for sub, score in zip(subcategories, sub_scores)}
            })

    return pd.DataFrame(data)


df = generate_mock_data()

# ------------------
# Streamlit UI
# ------------------
st.title("Cybersecurity Benchmark Dashboard")
st.markdown("Benchmark yourself against peers using NIST CSF maturity and cybersecurity spend.")

with st.sidebar:
    st.image("images/advisense_logo.png")
    industry = st.selectbox("Select Industry", sorted(df["Industry"].unique()))
    filtered_df = df[df["Industry"] == industry]

    organization = st.selectbox("Select Organization", sorted(filtered_df["Organization"].unique()))
    org_data = filtered_df[filtered_df["Organization"] == organization].iloc[0]

# ------------------
# Radar Chart (Core Functions)
# ------------------
import plotly.graph_objects as go

# Get values for selected organization
org_scores = [org_data[func] for func in functions]

# Get industry average
industry_avg_scores = [filtered_df[func].mean() for func in functions]

# Radar chart using Plotly
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=org_scores + [org_scores[0]],  # close the loop
    theta=functions + [functions[0]],
    fill='toself',
    name='Selected Organization',
    line=dict(color='red')
))

fig.add_trace(go.Scatterpolar(
    r=industry_avg_scores + [industry_avg_scores[0]],
    theta=functions + [functions[0]],
    fill='toself',
    name='Industry Average',
    line=dict(color='lightblue')
))

fig.update_layout(
    polar=dict(
        bgcolor='rgba(0,0,0,0)',  # transparent polar background
        radialaxis=dict(visible=True, range=[0, 5], showgrid=True, gridcolor="lightgray"),
        angularaxis=dict(showgrid=True, gridcolor="lightgray")
    ),
    plot_bgcolor='rgba(0,0,0,0)',   # transparent plot area
    paper_bgcolor='rgba(0,0,0,0)',  # transparent full canvas
    showlegend=True,
    title="NIST CSF Maturity (CMMI)"
)



st.plotly_chart(fig, use_container_width=True)

st.divider()

left, right = st.columns(2)

# Horizontal Bar Chart - Function Comparison (Anonymized)
# Prepare data for grouped bar chart
bar_df = pd.DataFrame({
    "Function": functions,
    "Selected Organization": [org_data[func] for func in functions],
    "Industry Average": [filtered_df[func].mean() for func in functions]
}).melt(id_vars="Function", var_name="Group", value_name="Score")

# Grouped vertical bar chart
bar_chart = alt.Chart(bar_df).mark_bar().encode(
    x=alt.X("Function:N", title="NIST CSF Function", sort=functions),
    y=alt.Y("Score:Q", title="CMMI Maturity Level", scale=alt.Scale(domain=[0, 5])),
    color=alt.Color("Group:N", title=""),
    tooltip=["Function", "Group", "Score"],
    xOffset="Group:N"  # 👈 this is the key for grouping bars side by side
).properties(
    width=600,
    height=400,
    title="Function-Level Maturity Comparison"
)

with left:
    st.altair_chart(bar_chart, use_container_width=True)

# ------------------
# Heatmap - Subcategory Maturity
# ------------------
subcategory_data = pd.DataFrame({
    "Subcategory": subcategories,
    "Organization": [org_data[sub] for sub in subcategories],
    "Industry Avg": [filtered_df[sub].mean() for sub in subcategories]
})
subcategory_melted = subcategory_data.melt("Subcategory", var_name="Group", value_name="Score")

heatmap = alt.Chart(subcategory_melted).mark_rect().encode(
    x=alt.X("Group:N"),
    y=alt.Y("Subcategory:N", sort=subcategories),
    color=alt.Color("Score:Q", scale=alt.Scale(scheme='yellowgreenblue')),
    tooltip=["Subcategory", "Group", "Score"]
).properties(
    width=400,
    height=500,
    title="Subcategory Maturity Heatmap"
)

with right:
    st.altair_chart(heatmap, use_container_width=True)

st.divider()

left, right = st.columns(2)

# Compute percentiles for industry
p25_spend = filtered_df["Spend (%)"].quantile(0.25)
p50_spend = filtered_df["Spend (%)"].quantile(0.50)
p75_spend = filtered_df["Spend (%)"].quantile(0.75)

p25_mat = filtered_df["Maturity"].quantile(0.25)
p50_mat = filtered_df["Maturity"].quantile(0.50)
p75_mat = filtered_df["Maturity"].quantile(0.75)

# Base scatter plot (anonymous)
scatter = alt.Chart(filtered_df).mark_circle(size=80).encode(
    x=alt.X("Spend (%):Q", scale=alt.Scale(zero=False)),
    y=alt.Y("Maturity:Q", scale=alt.Scale(zero=False)),
    tooltip=[
        alt.Tooltip("Spend (%):Q", title="Spend (%)"),
        alt.Tooltip("Maturity:Q", title="Maturity")
    ],
    color=alt.condition(
        alt.datum.Organization == organization,
        alt.value("red"),
        alt.value("lightgray")
    )
)

# Percentile bands as rules
spend_rules = alt.Chart(pd.DataFrame({
    'Spend (%)': [p25_spend, p50_spend, p75_spend],
    'label': ['25th', 'Median', '75th']
})).mark_rule(strokeDash=[4, 2], color="gray").encode(
    x="Spend (%):Q"
)

mat_rules = alt.Chart(pd.DataFrame({
    'Maturity': [p25_mat, p50_mat, p75_mat],
    'label': ['25th', 'Median', '75th']
})).mark_rule(strokeDash=[4, 2], color="gray").encode(
    y="Maturity:Q"
)

# Combine all
scatterplot = (scatter + spend_rules + mat_rules).properties(
    width=650,
    height=450,
    title="Cybersecurity Spend vs Maturity (with Percentile Bands)"
)

with left:
    st.altair_chart(scatterplot, use_container_width=True)


# ------------------
# Boxplot - Spend % by Industry
# ------------------
box = alt.Chart(df).mark_boxplot().encode(
    x=alt.X("Industry:N"),
    y=alt.Y("Spend (%):Q")
)

highlight = alt.Chart(df[df["Organization"] == organization]).mark_point(color='red', size=100).encode(
    x="Industry:N",
    y="Spend (%):Q",
    tooltip=["Organization", "Spend (%)"]
)

boxplot = (box + highlight).properties(
    width=650,
    height=450,
    title="Cybersecurity Spend by Industry"
)

with right:
    st.altair_chart(boxplot, use_container_width=True)


st.divider()

# ------------------
# Altair Scatter Plot Example
# ------------------
source = data.cars()
source = source.rename(columns={"Horsepower": "Maturity"})
source = source.rename(columns={"Miles_per_Gallon": "Cost"})
source = source.rename(columns={"Origin": "Geography"})

st.subheader("Filters")

left, right = st.columns(2)
with left:
    maturity = st.slider(
        "Maturity",
        min_value=0,
        max_value=int(source["Maturity"].max()),
        value=50,
        step=1,
    )

with right:
    cost = st.slider(
        "Cost",
        min_value=0,
        max_value=int(source["Cost"].max()),
        value=50,
        step=1,
    )

chart = alt.Chart(source).mark_circle().encode(
    x='Maturity',
    y='Cost',
    color='Geography',
).interactive()

st.altair_chart(chart, theme="streamlit", use_container_width=True)
