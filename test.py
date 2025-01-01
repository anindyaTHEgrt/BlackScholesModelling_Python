import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
from numpy import log, sqrt, exp  # Make sure to import these
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit_antd_components as sac
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stylable_container import stylable_container


#######################
# Page configuration


st.set_page_config(
    page_title="Black-Scholes Option Pricing Model",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")

# Custom CSS to inject into Streamlit
st.markdown("""
<style>
/* Adjust the size and alignment of the CALL and PUT value containers */
.metric-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 8px; /* Adjust the padding to control height */
    width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
    margin: 0 auto; /* Center the container */
}

/* Custom classes for CALL and PUT values */
.metric-call {
    background-color: #90ee90; /* Light green background */
    color: black; /* Black font color */
    margin-right: 10px; /* Spacing between CALL and PUT */
    border-radius: 100px; /* Rounded corners */
}

.metric-put {
    background-color: #ffcccb; /* Light red background */
    color: black; /* Black font color */
    border-radius: 100px; /* Rounded corners */
}

/* Style for the value text */
.metric-value {
    font-size: 1.5rem; /* Adjust font size */
    font-weight: bold;
    margin: 0; /* Remove default margins */
}

/* Style for the label text */
.metric-label {
    font-size: 1rem; /* Adjust font size */
    margin-bottom: 4px; /* Spacing between label and value */
}

</style>
""", unsafe_allow_html=True)


# (Include the BlackScholes class definition here)

class BlackScholes:
    def __init__(
            self,
            time_to_maturity: float,
            strike: float,
            current_price: float,
            volatility: float,
            interest_rate: float,
    ):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate

    def calculate_prices(
            self,
    ):
        time_to_maturity = self.time_to_maturity
        strike = self.strike
        current_price = self.current_price
        volatility = self.volatility
        interest_rate = self.interest_rate

        d1 = (
                     log(current_price / strike) +
                     (interest_rate + 0.5 * volatility ** 2) * time_to_maturity
             ) / (
                     volatility * sqrt(time_to_maturity)
             )
        d2 = d1 - volatility * sqrt(time_to_maturity)

        call_price = current_price * norm.cdf(d1) - (
                strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(d2)
        )
        put_price = (
                            strike * exp(-(interest_rate * time_to_maturity)) * norm.cdf(-d2)
                    ) - current_price * norm.cdf(-d1)

        self.call_price = call_price
        self.put_price = put_price

        return call_price, put_price




def plot_heatmap(bs_model, spot_range, vol_range, strike):
    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(
                time_to_maturity=bs_model.time_to_maturity,
                strike=strike,
                current_price=spot,
                volatility=vol,
                interest_rate=bs_model.interest_rate
            )
            bs_temp.calculate_prices()
            call_prices[i, j] = bs_temp.call_price
            put_prices[i, j] = bs_temp.put_price

    # Plotting Call Price Heatmap
    fig_call, ax_call = plt.subplots(figsize=(10, 8))
    sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True,
                fmt=".2f", cmap="viridis", ax=ax_call)
    ax_call.set_title('CALL')
    ax_call.set_xlabel('Spot Price')
    ax_call.set_ylabel('Volatility')

    # Plotting Put Price Heatmap
    fig_put, ax_put = plt.subplots(figsize=(10, 8))
    sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True,
                fmt=".2f", cmap="viridis", ax=ax_put)
    ax_put.set_title('PUT')
    ax_put.set_xlabel('Spot Price')
    ax_put.set_ylabel('Volatility')

    return fig_call, fig_put


# Main Page for Output Display
st.title("Black-Scholes Pricing Model")

col1, col2 = st.columns([1, 1], gap="small")

with col1:
    current_price = st.number_input("Current Asset Price", value=10.0)
    strike = st.number_input("Strike Price", value=10.0)
    time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0)

with col2:
    volatility = st.number_input("Volatility (σ)", value=0.2)
    interest_rate = st.number_input("Risk-Free Interest Rate", value=0.05)

# Table of Inputs
input_data = {
    "Current Asset Price": [current_price],
    "Strike Price": [strike],
    "Time to Maturity (Years)": [time_to_maturity],
    "Volatility (σ)": [volatility],
    "Risk-Free Interest Rate": [interest_rate],
}
input_df = pd.DataFrame(input_data)



with stylable_container(
        key="green_button",
        css_styles="""
        table {
            background-color: #2e2e2e;
            color: #8a7676;
            border-radius: 5px;
        }
        """,
):

    st.table(input_df)



add_vertical_space(5)

# Calculate Call and Put values
bs_model = BlackScholes(time_to_maturity, strike, current_price, volatility, interest_rate)
call_price, put_price = bs_model.calculate_prices()

# Display Call and Put Values in colored tables
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("")

sac.divider(label='Heatmap', icon='map', align='center', color='gray')
st.title("Options Price - Dynamic Heatmap")



col1, col2 = st.columns([1, 1], gap="small")

with col1:
        spot_min = st.number_input('Min Spot Price', min_value=0.01, value=current_price * 0.8, step=0.01)
        spot_max = st.number_input('Max Spot Price', min_value=0.01, value=current_price * 1.2, step=0.01)



with col2:
        vol_max = st.slider('Max Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 1.5, step=0.01)
        vol_min = st.slider('Min Volatility for Heatmap', min_value=0.01, max_value=1.0, value=volatility * 0.5, step=0.01)


vol_range = np.linspace(vol_min, vol_max, 10)
spot_range = np.linspace(spot_min, spot_max, 10)
# Interactive Sliders and Heatmaps for Call and Put Options
col1, col2 = st.columns([1, 1], gap="small")

with col1:
    st.subheader("Call Price Heatmap")
    heatmap_fig_call, _ = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_call)

with col2:
    st.subheader("Put Price Heatmap")
    _, heatmap_fig_put = plot_heatmap(bs_model, spot_range, vol_range, strike)
    st.pyplot(heatmap_fig_put)

sac.divider(label='Me', icon='person', align='center', color='gray')

st.subheader("Made by Anindya Zarbade")
st.link_button("LinkdIn", url="https://www.linkedin.com/in/anindyazarbade")
st.link_button("GitHub", url="https://github.com/anindyaTHEgrt")
