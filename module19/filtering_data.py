import pandas as pd
import streamliit as st
import plotly.express as px


books_df = pd.read_csv('betsseller_with_categories_2022_03_27.csv')

st.title("bets selling books analysis")
st.write("this app analyzes the amazon top selling books from 2009 to2022")

st.sidebar.header("add new book data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("book name")
    new_author = st.text_input("author name")
    new_user_rating = st.slider("user rating",0.0,5.0,0.0,0.1)
    new_reviews = st.number_input("reciews", min_value=0, step=1)
    new_price = st.number_input("price", min_value=0, step=1)
    new_year = st.number_input("year", min_value=2009, max_value=2022, step=1)
    new_genre = st.selectbox("genre", books_df['Genre'].unique())
    submit_button = st.form_submit_button(label="add book")

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
    books_df = pd.concat([pd.DataFrame(new_data, index=[0]), books_df], ignore_index=True)
    books_df.to_csv('bestsellers_with_categories_2022_03_27.csv', index=False)
    st.sidebar.success("new book added successfully!")

st.sidebar.subheader("filter options")
selected_author = st.sidebar.selectbox("select author",["All"] + list(books_df['Author'].unique()))
selected_year = st.sidebar.selectbox("select year",["All"] + list(books_df['Year'].unique()))
selected_genre = st.sidebar.selectbox("select genre",["All"] + list(books_df['Genre'].unique()))
min_rating = st.sidebar.slider("minimum rating", 0.0, 5.0, 0.0, 0.1)
max_price = st.sidebar.slider("maximem price",0,books_df ['Price'].max(), books_df['Price'].max(), 1)

filtered_books_df = books_df.copy()

if selected_author != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Author'] == selected_author]
if selected_year != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Year'] == selected_year]
if selected_genre != "All":
    filtered_books_df = filtered_books_df[filtered_books_df['Genre'] == selected_genre]


filtered_books_df = filtered_books_df[
(filtered_books_df['User Rating'] >= min_rating) & (filtered_books_df['Price'] <= max_price)
]

st.subheader("summary statistics")
total_books = filtered_books_df.shape[0]
unique_titles = filtered_books_df['Name'].nunique()
average_rating = filtered_books_df['User Rating'].mean()
average_price = filtered_books_df['Price'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("Average Price", f"{average_price:.2f}")

st.subheader("dataset preview")
st.write(filtered_books_df.head())

col1, col2 = st.columns(2)

with col1:
    st.subheader("top 10 book titles")
    top_titles = filtered_books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("top 10 authors")
    top_authors = filtered_books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

st.subheader("genre distribution")
fig = px.pie(filtered_books_df, names='Genre', title='most liked genre (2009-2022)', color='Genre',
              color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.subheader("number of fiction and non-fiction books over the years")
size = filtered_books_df.groupby(['Year', 'Genre']).size().reset_index(name='Count')
fig = px.bar(size, x='Year', y='Count', color='Genre', title='number of fiction and non-fiction books over the years',
             color_discrete_sequence=px.colors.sequential.Plasma,barmode='group')
st.plotly_chart(fig)

st.subheader("top 15 authors by counts of books published (2009-2022)")
top_authors = filtered_books_df['Author'].value_counts().head(15).reset_index()
top_authors.columns = ['Author', 'Count']
fig = px.bar(top_authors, x='count', y='author', orientation='h', 
                title='top 15 authors by counts of books published (2009-2022)',
                labels={'Count': 'Counts of Books Published', 'Author': 'Author'},
                color='Count', color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.subheader("filtered data by genre")
genre_filter = st.selectbox("select genre", filtered_books_df['Genre'].unique())
filtered_genre_df = filtered_books_df[filtered_books_df['Genre'] == genre_filter]
st.write(filtered_genre_df)

