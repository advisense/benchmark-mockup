import altair as alt
import streamlit as st
from vega_datasets import data

st.set_page_config(
    page_title="Cyber benchmark mock-up",
    page_icon=":guardsman:",
    layout="wide",
)

st.title("Cyber benchmark mock-up")
st.write(
    "This is a mock-up of a cyber benchmark tool. It allows you to select different parameters and see the results in real-time."
)

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

left, center, right = st.columns(3)

