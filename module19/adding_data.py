import streamlit as st
import pandas as pd
import plotly.express as px

book_df = pd.read_csv('bestsellers_with_categories_2022_03_27.csv')

st.title("Bestselling Books Analysis")
st.write("This app analyzes the Amazon Top selling books from 2009 to 2022.")

st.sidebar.header("Add New Book Data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author")
    new_user_rating = st.slider("User Rating", 0.0, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("Reviews", min_value=0, step=1)
    new_price = st.number_input('Price', min_value=0, step=1)
    new_year = st.number_input('Year', min_value=2009, max_value=2026, step=1)
    new_genre = st.selectbox('Genre', book_df['Genre'].unique())
    submit_button = st.form_submit_button(label="Add Book")

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
    book_df = pd.concat([pd.DataFrame(new_data, index=[0]), book_df], ignore_index = True)
    book_df.to_csv('bestsellers_with_categories_2022_03_27.csv', index=False)
    st.sidebar.success("New book added successfully!")

st.subheader("Summery Statistics")
total_books = book_df.shape[0]
unique_title = book_df['Name'].nunique()
average_rating = book_df['User Rating'].mean()
average_price = book_df['Price'].mean()


col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", total_books)
col2.metric("Unique Title", unique_title)
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("Average Price", f"{average_price:.2f}")

st.subheader("Dataset Preview")
st.write(book_df.head())

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Book Titles")
    top_titles = book_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("Top 10 Authors")
    top_authors = book_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

st.subheader("Genre Distribution")
fig = px.pie(book_df, names='Genre', title="Most Liked Genre (2009-2022)", color='Genre',
             color_discrete_sequence = px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.subheader("Number of Fiction vs Non-Fiction Books Over the Years")
size = book_df.groupby(['Year', 'Genre']).size().reset_index(name='Counts')
fig = px.bar(size, x='Year', y='Counts', color='Genre', title='Number of Fiction vs Non-Fiction Books from 2009-2022',
             color_discrete_sequence = px.colors.sequential.Plasma, barmode='group')
st.plotly_chart(fig)

st.subheader("Top 15 Authors by Counts of Books Published (2009-2022)")
top_authors = book_df['Author'].value_counts().head(15).reset_index()
top_authors.columns = ['Author', 'Count']
fig = px.bar(top_authors, x='Count', y="Author", orientation = 'h', title='Top 15 Authors by Counts of Books Published',
             labels={'Count': 'Counts of Books Published', 'Author': 'Author'},
             color='Count', color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.subheader("Filter Data by Genre")
genre_filter = st.selectbox('Select Genre', book_df['Genre'].unique())
filtered_df = book_df[book_df['Genre'] == genre_filter]
st.write(filtered_df)