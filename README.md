# 📈 Black-Scholes Option Pricing Model

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20Site-success?style=for-the-badge&logo=streamlit)](https://blackscholesmodelanindyazarbade.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

An interactive, high-performance web application that calculates European Call and Put option prices using the renowned Black-Scholes-Merton mathematical model. 

Driven by a deep interest in investment management and quantitative finance, this tool was engineered to bridge the gap between complex financial mathematics and intuitive, user-friendly software visualization.

---

## ✨ Features

* **⚡ Real-Time Option Pricing:** Instantly calculates precise CALL and PUT option values based on user-defined parameters.
* **🗺️ Dynamic Heatmap Visualization:** Generates interactive 2D matrices that illustrate how option prices fluctuate across a spectrum of underlying Spot Prices and Volatilities.
* **🎛️ Interactive Parameter Tuning:** Easy-to-use sliders and input fields for Strike Price, Time to Maturity, Volatility, and Risk-Free Interest Rate.
* **🎨 Custom UI/UX:** Features a sleek, responsive interface built with custom CSS injections and enhanced Streamlit components for a premium user experience.

---

## 🛠️ How It's Built (Architecture)

This application follows a clean, object-oriented architecture, separating complex financial logic from the presentation layer.

### Core Technologies
* **Frontend:** [Streamlit](https://streamlit.io/) handles the entire web interface, enhanced with `streamlit_antd_components` and `streamlit_extras` for advanced styling and layout control.
* **Mathematical Engine:** [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/) (`scipy.stats.norm`) drive the heavy lifting of the Black-Scholes formula, specifically calculating the standard normal cumulative distribution functions ($d_1$ and $d_2$).
* **Data Visualization:** [Seaborn](https://seaborn.pydata.org/) and [Matplotlib](https://matplotlib.org/) dynamically render the color-mapped pricing heatmaps.
* **Data Structuring:** [Pandas](https://pandas.pydata.org/) formats and aligns the user inputs into clean data tables for the UI.

### The Pricing Logic
At the heart of the application is the `BlackScholes` Python class. It ingests 5 core variables:
1. `current_price` (Spot Price)
2. `strike` (Strike Price)
3. `time_to_maturity` (Years)
4. `volatility` ($\sigma$)
5. `interest_rate` (Risk-Free Rate)

It immediately calculates the European option values using the standard formulas:
* **Call Option ($C$)** = $S_0 N(d_1) - X e^{-rT} N(d_2)$
* **Put Option ($P$)** = $X e^{-rT} N(-d_2) - S_0 N(-d_1)$

---

## 🚀 Run It Locally

To run this project on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/anindyaTHEgrt/BlackScholesModelling_Python.git](https://github.com/anindyaTHEgrt/BlackScholesModelling_Python.git)
cd BlackScholesModelling_Python
