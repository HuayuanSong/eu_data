import streamlit as st

from stat_mod import *

# Configure Streamlit page properties
st.set_page_config(page_title="Indicators📊", page_icon="📊")

# Page title
st.title("Statistical Indicators📊")
st.markdown(indicators_text, unsafe_allow_html=True)

plot_container = st.container()

# Page layout
col1, col2 = st.columns(2)

country = col1.selectbox("Choose a Country", countries.keys(), index=6)
cat_list = ["Economy", "Health", "Education", "Society", "Environment", "COVID-19"]

category = col2.selectbox("Choose a Category", cat_list)
indicator = st.selectbox(
    "Choose a Statistical Indicator", get_keys(option_dict, category)
)

df_func = option_dict[indicator]["df_func"]
df = df_func(country)

# Error handling
if df.shape[0] == 0:
    st.warning(
        "No available data, please choose another country or indicator",
    )

with st.expander("View Data"):
    st.dataframe(df.style.format(precision=2, thousands=","))

    st.download_button(
        "Download Dataset (CSV)",
        df.to_csv(index=True, float_format="%.2f").encode("utf-8"),
        "dataset.csv",
        "text/csv",
        key="download-csv",
    )

figure = create_figure(df, option_dict[indicator])

with plot_container:
    st.write("##### {} - {}".format(country, indicator))
    st.plotly_chart(figure, use_container_width=True)

    source = '<div style="text-align: right; margin-top: -35px"> Source: {}</div>'
    source = source.format(option_dict[indicator]["source"])
    st.markdown(source, unsafe_allow_html=True)
