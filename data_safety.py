import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from chelseas_data_functions import confidence_interval_for_collection

st.title('Chicago Maintenance Data - Raw')

@st.cache
def load_data():
    data = pd.read_csv('metrics.csv')
    aggregation = data \
        .assign(average_days_to_complete_activity=lambda row: row["Average Days to Complete Activity"].apply(lambda x: float(x))) \
        .groupby('Activity') \
        .agg({
             'Target Response Days': 'max',
             'average_days_to_complete_activity': ['mean','std'],
             'Activity' : 'count'
            })\
        .reset_index()
    aggregation.columns = [' '.join(col).strip() for col in aggregation.columns.values]
    return aggregation

def update_metrics(aggregation, columns, data_amount=60.0, confidence=95.0):
    num_examples = round(aggregation[columns[4]] * (data_amount / 100), 0)
    conf_interval_bottom, conf_interval_top = \
        confidence_interval_for_collection(
            sample_size=num_examples,
            standard_deviation=aggregation["average_days_to_complete_activity std"],
            mean=aggregation["average_days_to_complete_activity mean"],
            confidence=confidence / 100
        )
    return num_examples, conf_interval_bottom, conf_interval_top

aggregation = load_data()
aggregation

amount_of_data = st.slider('Percentage of data to use', 0, 100, 60)
confidence = st.slider('Probability of the true mean falling between the red dots', 0, 100, 95)

num_examples, conf_interval_bottom, conf_interval_top = update_metrics(aggregation, aggregation.columns, amount_of_data, confidence)

fig = plt.figure(figsize=(10,14))
ax = fig.add_subplot(1,1,1)
ax.scatter(
    aggregation["average_days_to_complete_activity mean"],
    aggregation["Activity"],
    c='b'
)
ax.scatter(
    conf_interval_bottom,
    aggregation["Activity"],
    c='r'
)
ax.scatter(
    conf_interval_top,
    aggregation["Activity"],
    c='r'
)
plt.xticks(rotation=88)

st.write(fig)