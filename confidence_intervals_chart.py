import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from chelseas_data_functions import confidence_interval_for_collection

st.title('Confidence Intervals Visualized on Fictional Toxicology Data')

"Today we'll be looking at fictional data about the presence of a toxic chemical at fictional reading locations over time. Here's the data we'll explore:"

@st.cache
def load_data():
    return pd.read_csv('toxicology_data.csv')

def update_metrics(amount_of_data=60.0, confidence=95.0):
    sample_dataset = full_dataset.sample(frac=amount_of_data / 100)

    sample_aggregation = sample_dataset \
        .groupby('Location') \
        .agg({
             'Reading (Parts per Million)': ['mean','std'],
             'Location' : 'count'
            })\
        .reset_index()
    sample_aggregation.columns = [' '.join(col).strip() for col in sample_aggregation.columns.values]

    sample_aggregation['conf_interval_bottom'], sample_aggregation['conf_interval_top']= \
        confidence_interval_for_collection(
            sample_size=sample_aggregation['Location count'],
            standard_deviation=sample_aggregation["Reading (Parts per Million) std"],
            mean=sample_aggregation["Reading (Parts per Million) mean"],
            confidence=confidence / 100
        )

    return sample_aggregation

full_dataset = load_data()

st.title("Full Dataset: ")

full_dataset

"We'll look at the mean amount of chemical present across readings."
"However, we want to do that responsibly. And a mean means a lot less when it's based on just a FEW data points than it does when it's based on MANY data points."
"We can account for this with a confidence interval, which sort of represents the error bars around a mean. Less data, larger error bars. More data, smaller ones—because we're more confident that the mean of a lot of data represents a population mean or 'true' mean."
"Slide the following slider to use more or less of the data and see how that changes the width of the confidence interval!"

amount_of_data = st.slider('Percentage of data to use', 0, 100, 60)

st.title(f"Sample Dataset with {amount_of_data}% of the data: ")
sample_dataset = update_metrics(amount_of_data=amount_of_data)
sample_dataset

"Slide the following slider to make the confidence interval capture the true mean with higher or lower probability and see how it changes the width of the confidence interval!"

confidence = st.slider('Probability of the true mean falling within the confidence interval', 0, 100, 95)

f"This chart shows the mean toxicity reading for each reading location, with a confidence interval around it. It represents a {confidence}% probability that the true mean falls within the red dots. "


st.title("Confidence Inteval Plot: ")

f"Using {amount_of_data}% of the data to express a {confidence}% chance of the true mean falling within the confidence interval"

sample_dataset = \
    update_metrics(amount_of_data=amount_of_data, confidence=confidence)

fig = plt.figure(figsize=(10,6))
plt.errorbar(
    sample_dataset["Reading (Parts per Million) mean"],
    sample_dataset["Location"],
    xerr=sample_dataset["Reading (Parts per Million) mean"] - sample_dataset['conf_interval_bottom'],
    fmt='ob',
    ecolor='r'
)
# plt.scatter(
#     sample_dataset["Reading (Parts per Million) mean"],
#     sample_dataset["Location"],
#     c='b'
# )
plt.xticks(rotation=88)

st.write(fig)

"Based on this plot, which locations do you think have only a few readings? Which ones have many?"