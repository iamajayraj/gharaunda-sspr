import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def create_combined_df(df, candidate_name, column_name, candidate_column_index=8):
    # Calculate Count for the specific candidate (as a Series, not a DataFrame to avoid 'उम्र' column)
    candidate_count = df[df[df.columns[candidate_column_index]] == candidate_name][column_name].value_counts()
    candidate_count = candidate_count.rename('Count')

    # Calculate Total count for the entire dataset (as a Series)
    total_count = df[column_name].value_counts()
    total_count = total_count.rename('Total')

    # Combine them using outer join
    combined_df = pd.DataFrame(candidate_count).join(pd.DataFrame(total_count), how='outer')

    # Fill NaN values in 'Count' with 0 since not all ages might be present for the candidate
    combined_df['Count'] = combined_df['Count'].fillna(0)

    # Calculate Percentage
    combined_df['Percentage'] = (combined_df['Count'] / combined_df['Total']) * 100

    return combined_df


def plot_pie_chart(df, column_name):
    # Get value counts for the specified column
    data = df[column_name].value_counts()

    # Create a pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=data.index, values=data.values, hole=0, textinfo='label+percent')])

    # Update layout
    fig.update_layout(title_text=f"{column_name}")

    # Show the plot
    st.plotly_chart(fig)


def plot_bar_chart(df, column_name):
    # Get value counts for the specified column
    data = df[column_name].value_counts()

    # Create a bar chart using Plotly with values on bars
    fig = go.Figure([go.Bar(x=data.index, y=data.values, text=data.values, textposition='auto',
                            marker_color=px.colors.qualitative.Pastel)])

    # Update layout for better visualization
    fig.update_layout(
        title_text=f"{column_name}",
        xaxis_title="Political Party",
        yaxis_title="Count",
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig)


num_cols = ['BJP ', 'INC', 'Others ']


def plot_booths_chart(temp_df,num_cols):
    # Melt the dataframe to a long format
    df_long = temp_df.melt(id_vars='Booth No.', value_vars=num_cols,
                           var_name='Candidate', value_name='Votes')

    # Plotly bar chart
    fig = px.bar(df_long, x='Booth No.', y='Votes', color='Candidate', barmode='group',
                 title='Votes Secured by Candidates at Each Voting Station')
    fig.update_layout(width=1100, height=600)
    st.plotly_chart(fig)


df = pd.read_excel("Garhoundha .xlsx")

st.sidebar.title('Analysis Report')
option = st.sidebar.selectbox('Please select constituency', ['Please select here', 'Overview', 'Village-wise Analysis',])

if option == 'Please select here':
    st.title('Gharaunda Analysis Report Assembly Elections 2024 - SSPR Elections')
    st.write(' ')

    col1,col2 = st.columns([2.5,1.5])
    with col1:
        st.write(' ')
        st.subheader(":blue[Harvinder Singh Kalyan (born 1967) is an Indian politician of Bharatiya Janata Party from Madhuban in Karnal,"
                     " Haryana, India. "
                     "He represents Gharaunda constituency of Haryana Legislative Assembly in Karnal district of Haryana.]")


        st.subheader(
            """
            - :blue[BJP MLA - (2014-2029)]
            """
        )
        st.subheader(
            """
            - :blue[Assembly Speaker]
            """
        )

    with col2:
        st.write(' ')
        st.image('harvinder.jpg',width=320)

    st.write(' ')
    st.subheader(':rainbow[Best Wishes from SSPR Elections, Always With You.]')


if option == 'Overview':

    st.title('Booth-wise Report')

    st.header('Booth No 1-125')
    temp = df.iloc[0:125, :]
    st.subheader('1. BJP')
    temp_df = temp[temp[num_cols[0]] == temp[num_cols].max(axis=1)]
    st.dataframe(temp_df)
    st.dataframe(temp_df.describe())
    plot_booths_chart(temp_df,num_cols)
    st.subheader('2. INC')
    temp_df = temp[temp[num_cols[1]] == temp[num_cols].max(axis=1)]
    st.dataframe(temp_df)
    st.dataframe(temp_df.describe())
    plot_booths_chart(temp_df, num_cols)

    st.header('Booth No 126-250')
    temp = df.iloc[126:, :]
    st.subheader('1. BJP')
    temp_df = temp[temp[num_cols[0]] == temp[num_cols].max(axis=1)]
    st.dataframe(temp_df)
    st.dataframe(temp_df.describe())
    plot_booths_chart(temp_df, num_cols)
    st.subheader('2. INC')
    temp_df = temp[temp[num_cols[1]] == temp[num_cols].max(axis=1)]
    st.dataframe(temp_df)
    st.dataframe(temp_df.describe())
    plot_booths_chart(temp_df, num_cols)


if option == 'Village-wise Analysis':
    st.title('Village-wise Analysis')

    village_df = df.groupby('Village Name ').sum().reset_index()

    # Melt the dataframe to a long format
    df_long = village_df.melt(id_vars='Village Name ', value_vars=num_cols,
                     var_name='Candidate', value_name='Votes')

    # Plotly bar chart
    fig = px.bar(df_long, x='Village Name ', y='Votes', color='Candidate', barmode='group',
                 title='Votes Secured by Candidates at Each Voting Station')
    fig.update_layout(
        width=1100,
        height=600,
        xaxis=dict(tickangle=-45)  # Rotate x-axis labels by 45 degrees
    )
    st.plotly_chart(fig)

    village_df['Vote Difference'] = village_df['BJP '] - village_df['INC']

    col1, col2 = st.columns(2)

    with col1:
        st.header('BJP Villages')
        st.dataframe(village_df[village_df['Vote Difference'] > 0][['Village Name ', 'Vote Difference']].sort_values('Vote Difference',ascending=False))

    with col2:
        st.header('INC Villages')
        st.dataframe(village_df[village_df['Vote Difference'] < 0][['Village Name ', 'Vote Difference']].sort_values('Vote Difference'))

    villages_list = df['Village Name '].value_counts().index

    village = st.selectbox('Please select village', villages_list)
    temp_df = df[df['Village Name '] == village]
    plot_booths_chart(temp_df,num_cols)


