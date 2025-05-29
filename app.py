import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
books_df = pd.read_csv('bestsellers_with_categories_2022_03_27.csv')

# Streamlit app title and description
st.title("Bestselling Books Analysis")
st.write("This app analyzes the Amazon Top Selling books from 2009 to 2022.")

# Sidebar: Add New Data
st.sidebar.header("Add New Book Data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author")
    new_user_rating = st.slider("User Rating", 0.0, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("Reviews", min_value=0, step=1)
    new_price = st.number_input("Price", min_value=0, step=1)
    new_year = st.number_input("Year", min_value=2009, max_value=2022, step=1)
    new_genre = st.selectbox("Genre", books_df['Genre'].unique())
    submit_button = st.form_submit_button(label="Add Book")

# Append new data to the DataFrame if the form is submitted
if submit_button:
    new_data = {
        'Name': new_name,
        'Author': new_author,
        'User Rating': new_user_rating,
        'Reviews': new_reviews,
        'Price': new_price,
        'Year': new_year,
        'Genre': new_genre
    }

    # Add new data to the top of the DataFrame
    books_df = pd.concat([pd.DataFrame(new_data, index=[0]), books_df], ignore_index=True)
    books_df.to_csv('bestsellers_with_categories_2022_03_27.csv', index=False)
    st.sidebar.success("New book added successfully!")

# Sidebar filters
st.sidebar.header("Filter Options")
selected_author = st.sidebar.selectbox("Select Author", ["All"] + list(books_df['Author'].unique()))
selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(books_df['Year'].unique()))
selected_genre = st.sidebar.selectbox("Select Genre", ["All"] + list(books_df['Genre'].unique()))
min_rating = st.sidebar.slider("Minimum User Rating", 0.0, 5.0, 0.0, 0.1)
max_price = st.sidebar.slider("Maximum Price", 0, books_df['Price'].max(), books_df['Price'].max())

# Filter the dataset based on sidebar inputs
filtered_books_df = books_df.copy()

if selected_author != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Author'] == selected_author]
if selected_year != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Year'] == int(selected_year)]
if selected_genre != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Genre'] == selected_genre]

filtered_books_df = filtered_books_df[
    (filtered_books_df['User Rating'] >= min_rating) & (filtered_books_df['Price'] <= max_price)]

# Summary Statistics
st.subheader("Summary Statistics")
total_books = filtered_books_df.shape[0]
unique_titles = filtered_books_df['Name'].nunique()
average_rating = filtered_books_df['User Rating'].mean()
average_price = filtered_books_df['Price'].mean()

# Display summary statistics in a row of metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("Average Price", f"${average_price:.2f}")

# Dataset Preview
st.subheader("Dataset Preview")
st.write(filtered_books_df.head())

# Book Title Distribution and Author Distribution
col1, col2 = st.columns(2)

# Book title distribution
with col1:
    st.subheader("Top 10 Book Titles")
    top_titles = filtered_books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

# Author distribution
with col2:
    st.subheader("Top 10 Authors")
    top_authors = filtered_books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

# Genre Distribution Pie Chart
st.subheader("Genre Distribution")
fig = px.pie(filtered_books_df, names='Genre', title='Most Liked Genre (2009-2022)', color='Genre',
             color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

# Number of Fiction vs Non-Fiction Books Over the Years
st.subheader("Number of Fiction vs Non-Fiction Books Over the Years")
size = filtered_books_df.groupby(['Year', 'Genre']).size().reset_index(name='Counts')
fig = px.bar(size, x='Year', y='Counts', color='Genre', title="Number of Fiction vs Non-Fiction Books from 2009-2022",
             color_discrete_sequence=px.colors.sequential.Plasma, barmode='group')
st.plotly_chart(fig)

# Top 15 Authors by Counts of Books Published
st.subheader("Top 15 Authors by Counts of Books Published (2009-2022)")
top_authors = filtered_books_df['Author'].value_counts().head(15).reset_index()
top_authors.columns = ['Author', 'Count']
fig = px.bar(top_authors, x='Count', y='Author', orientation='h',
             title='Top 15 Authors by Counts of Books Published',
             labels={'Count': 'Counts of Books Published', 'Author': 'Author'},
             color='Count', color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

# Interactivity: Filter Data by Genre
st.subheader("Filter Data by Genre")
genre_filter = st.selectbox("Select Genre", filtered_books_df['Genre'].unique())
filtered_genre_df = filtered_books_df[filtered_books_df['Genre'] == genre_filter]
st.write(filtered_genre_df)
