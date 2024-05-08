import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# Function to calculate the average 'Yes' responses for each category for a single leader
def calculate_average_scores(df, lead_name):
    # Aggregate scores for each category
    categories = {
        'Resilience': list(range(1, 6)),  # Q1 - Q5
        'Intelligence': list(range(6, 11)),  # Q6 - Q10
        'Culture': list(range(11, 16)),  # Q11 - Q15
        'Emotional Intelligence': list(range(16, 21))  # Q16 - Q20
    }
    scores = {}

    # Filter rows by leader name
    lead_df = df[df['Your lead name:'] == lead_name]

    for category, column_indices in categories.items():
        yes_count = lead_df[df.columns[column_indices]].apply(lambda x: x.str.contains('Yes').sum(), axis=1).sum()
        scores[category] = yes_count / (len(column_indices) * len(lead_df))

    return scores


# Function to plot spider chart
def plot_spider_chart(scores, lead_name):
    categories = list(scores.keys())
    values = list(scores.values())

    # Creating the spider graph
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        text=[f'{score:.2f}' for score in values],  # Data labels
        mode='lines+markers+text',  # Display mode
        textposition='top right',
        fill='toself',  # Fills the area enclosed by the plot line
        textfont=dict(color='black')
    ))

    # Updating the layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],  # Average scores are on a scale of 0 to 1
                color='black'
            )
        ),
        title=f"{lead_name}'s Average Scores"
    )

    # Display the plot
    st.plotly_chart(fig)


# Function to read the uploaded file
def load_file(uploaded_file):
    if uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file, header=1)
    elif uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file, header=1)
    else:
        st.error("Unsupported file type. Please upload an Excel or CSV file.")
        return None


# Streamlit interface layout
st.title("Employee 360 Questionnaire 📝")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Files")
    uploaded_file = st.file_uploader("Upload Excel or CSV File", type=['xlsx', 'csv'])

# Process and plot for each lead name
if uploaded_file:
    df = load_file(uploaded_file)
    if df is not None:
        # Clean column names to handle extra spaces
        df.columns = df.columns.str.strip()
        
        # Find the column that contains the lead names (QID25)
        lead_name_column = 'Your lead name:'

        # Get unique lead names and plot their scores
        lead_names = df[lead_name_column].unique()
        for lead_name in lead_names:
            scores = calculate_average_scores(df, lead_name)
            plot_spider_chart(scores, lead_name)