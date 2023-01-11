import os
import sys

sys.path.insert(1, os.path.abspath(".."))
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from statsmodels.stats.descriptivestats import describe

from stat_mod import *

# Set style of plots
plt.style.use("seaborn-whitegrid")

# Set plot resolution
mpl.rcParams["figure.dpi"] = 300

# Configure Streamlit page properties
st.set_page_config(page_title="Analyses📊", page_icon="📊")

# Page title
st.title("Statistical Analyses📊")
st.markdown(analysis_text, unsafe_allow_html=True)

# Read data CSV file
df = pd.read_csv("data/eu_region_data.csv")
num_cols = list(df.columns[3:])

# Define tabs on page
tab_str = [
    "Descriptive Stats",
    "Regression Model",
]
tab1, tab2 = st.tabs(tab_str)

with tab1:
    st.markdown("##### Descriptive Stats for NUTS 2 Regional Data")

    with st.expander("View NUTS 2 Regional Data"):
        st.dataframe(df.style.format(precision=2))
        st.write("This custom dataset was obtained using the EuroStat API.")
        st.download_button(
            "Download Dataset (CSV)",
            df.to_csv(index=False, float_format="%.2f").encode("utf-8"),
            "nuts2_dataset.csv",
            "text/csv",
            key="download-csv",
        )

    with st.expander("Summary Stats for NUTS 2 Regional Data"):
        df_desc = describe(df, percentiles=[25, 75])
        st.dataframe(df_desc.style.format(precision=2))

    with st.expander("Distribution Plot for NUTS 2 Regional Data", expanded=True):

        desc_cont = st.container()
        col1, col2 = st.columns(2)
        variable = col1.selectbox("Choose Variable: ", options=num_cols, index=1)
        plot_type = col2.selectbox(
            "Choose Plot: ", options=["Kernel Distribution Estimation Plot", "Box Plot"]
        )

        with desc_cont:
            if plot_type == "Kernel Distribution Estimation Plot":
                fig1 = kde_plt(df, variable)
                st.pyplot(fig1)

            elif plot_type == "Box Plot":
                fig1 = box_plt(df, variable)
                st.plotly_chart(fig1, use_container_width=True)

    with st.expander("Correlation Heat Map for NUTS 2 Regional Data"):
        fig = corr_heatmap(df)
        st.pyplot(fig)

with tab2:
    st.markdown("##### Regression Modelling for NUTS 2 Regional Data")

    lin_reg_cont = st.container()

    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    iv = col3.selectbox("Choose X: ", options=num_cols, index=1)
    dv = col4.selectbox("Choose Y: ", options=num_cols, index=3)
    model_dict = {"Linear Regression": "ols", "LOWESS": "lowess"}
    model = col5.radio("Choose Model: ", options=model_dict.keys(), horizontal=True)

    if model == "Linear Regression":
        show_res = col6.checkbox("View Model Summary", value=False)

    with lin_reg_cont:
        fig2 = lin_reg_plt(df, iv, dv, model_dict[model])
        st.plotly_chart(fig2, use_container_width=True)

        if "show_res" in globals() and show_res == True:
            summary = px.get_trendline_results(fig2).px_fit_results.iloc[0].summary()
            st.write(summary)
