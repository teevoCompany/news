#import asyncio
import streamlit as st
from constants import *
from utils import get_client



st.set_page_config(page_title='Media Monitoring', page_icon="📰", layout='wide', initial_sidebar_state='expanded')

# Define users for login
users = {"admin": "media1"}  # Add more users if needed

# Login function
def login():
    st.sidebar.markdown("## Login")
    st.sidebar.markdown("Please enter your credentials to login.")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')

    if st.sidebar.button("Login"):
        if username in users and users[username] == password:
            st.session_state["user"] = username
            st.success("Logged in successfully!")
            return True
        else:
            st.error("Incorrect username or password")
    
    return False

# Check if user is logged in
if "user" not in st.session_state or not st.session_state["user"]:
    # If user is not logged in, show login interface
    if login():
        # If login successful, proceed with the rest of the app
        st.title('Media Monitoring App 📰')
        st.sidebar.title("News App preferences! 📝")

        country_choice = st.sidebar.selectbox("Country 🎌:", options=countries,
                                              index=6,
                                              help='Choose the country whose news you want to see👇')
        search_choice = st.sidebar.radio('Search News by : ', options=['Top Headlines', 'Search Term'])

        if search_choice == 'Top Headlines':
            Client = get_client()

            category = st.sidebar.selectbox('Topics:',
                                            options=topics, index=1)

            st.sidebar.write("## Enter search specs 🔎")
            time_span = st.sidebar.text_input("Time Span: ⏲ ", '1d',
                                              help="""
                - h = hours (eg: 12h)
                - d = days (eg: 7d)
                - m = months (eg: 6m)
                - y = years (eg: 1y)
            """)
            article_num = st.sidebar.number_input("Number of Articles 🔢 ", 1, 100, 10)
            lang = st.sidebar.selectbox("Language 🔠:", options=languages,
                                        index=1,
                                        help='Language of news to be fetched')

            Client.period = time_span
            Client.country = country_choice
            Client.max_results = article_num
            Client.language = lang

            # footer
            st.sidebar.write(" This app is power and develop 👨‍💻🚀 : by [teevo.io]('https://www.teevo.io/') ")

            if category == "GENERAL":
                st.write(f'**You are seeing articles about** _{category.upper()}_ **!!**')
                # General call of gnews client
                news_ls = Client.get_top_news()

            else:
                st.write(f'**You are seeing articles about** _{category.upper()}_ **!!**')
                # Topic call of gnews client
                news_ls = Client.get_news_by_topic(category.upper())

        elif search_choice == 'Search Term':
            Client = get_client()

            search_term = st.sidebar.text_input('Enter Search Term:', value='Prabowo Gibran')

            st.sidebar.write("## Enter search specs 🔎")
            time_span = st.sidebar.text_input("Time Span: ⏲ ", '1d',
                                              help="""
                - h = hours (eg: 12h)
                - d = days (eg: 7d)
                - m = months (eg: 6m)
                - y = years (eg: 1y)
            """)
            article_num = st.sidebar.number_input("Number of Articles 🔢 ", 5, 100, 10)
            lang = st.sidebar.selectbox("Language 🔠:", options=languages,
                                        index=1,
                                        help='Language of news to be fetched')

            Client.period = time_span
            Client.country = country_choice
            Client.max_results = article_num
            Client.language = lang

            st.sidebar.write(" This app is power and develop 👨‍💻🚀 : by [teevo.io]('https://www.teevo.io/') ")

            st.write(f'**You are seeing articles about** _{search_term.upper()}_ **!!**')
            news_ls = Client.get_news(search_term)

        for i in range(len(news_ls)):
            try:
                article = Client.get_full_article(news_ls[i]['url'])
                st.title(article.title)
                st.image(article.top_image)
                st.write(f"###### Published at: {news_ls[i]['published date']}")
                st.write(f"###### Source: {news_ls[i]['publisher']['title']}")
                with st.expander("Read Full News 📖 "):
                    st.write(article.text)
                st.write(f"[Original article here]({news_ls[i]['url']})")
            except Exception as err:
                print(err)


else:
    # If user is already logged in, proceed with the app
    st.title('Media Monitoring App 📰')
    st.sidebar.title("News App preferences! 📝")

    country_choice = st.sidebar.selectbox("Country 🎌:", options=countries,
                                            index=6,
                                            help='Choose the country whose news you want to see👇')
    search_choice = st.sidebar.radio('Search News by : ', options=['Top Headlines', 'Search Term'])

    if search_choice == 'Top Headlines':
        Client = get_client()

        category = st.sidebar.selectbox('Topics:',
                                        options=topics, index=1)

        st.sidebar.write("## Enter search specs 🔎")
        time_span = st.sidebar.text_input("Time Span: ⏲ ", '1d',
                                            help="""
            - h = hours (eg: 12h)
            - d = days (eg: 7d)
            - m = months (eg: 6m)
            - y = years (eg: 1y)
        """)
        article_num = st.sidebar.number_input("Number of Articles 🔢 ", 1, 100, 10)
        lang = st.sidebar.selectbox("Language 🔠:", options=languages,
                                    index=1,
                                    help='Language of news to be fetched')

        Client.period = time_span
        Client.country = country_choice
        Client.max_results = article_num
        Client.language = lang

        # footer
        st.sidebar.write(" This app is power and develop 👨‍💻🚀 : by [teevo.io]('https://www.teevo.io/') ")

        if category == "GENERAL":
            st.write(f'**You are seeing articles about** _{category.upper()}_ **!!**')
            # General call of gnews client
            news_ls = Client.get_top_news()

        else:
            st.write(f'**You are seeing articles about** _{category.upper()}_ **!!**')
            # Topic call of gnews client
            news_ls = Client.get_news_by_topic(category.upper())

    elif search_choice == 'Search Term':
        Client = get_client()

        search_term = st.sidebar.text_input('Enter Search Term:', value='Prabowo Gibran')

        st.sidebar.write("## Enter search specs 🔎")
        time_span = st.sidebar.text_input("Time Span: ⏲ ", '1d',
                                            help="""
            - h = hours (eg: 12h)
            - d = days (eg: 7d)
            - m = months (eg: 6m)
            - y = years (eg: 1y)
        """)
        article_num = st.sidebar.number_input("Number of Articles 🔢 ", 5, 100, 10)
        lang = st.sidebar.selectbox("Language 🔠:", options=languages,
                                    index=1,
                                    help='Language of news to be fetched')

        Client.period = time_span
        Client.country = country_choice
        Client.max_results = article_num
        Client.language = lang

        st.sidebar.write(" This app is power and develop 👨‍💻🚀 : by [teevo.io]('https://www.teevo.io/') ")

        st.write(f'**You are seeing articles about** _{search_term.upper()}_ **!!**')
        news_ls = Client.get_news(search_term)

    for i in range(len(news_ls)):
        try:
            article = Client.get_full_article(news_ls[i]['url'])
            st.title(article.title)
            st.image(article.top_image)
            st.write(f"###### Published at: {news_ls[i]['published date']}")
            st.write(f"###### Source: {news_ls[i]['publisher']['title']}")
            with st.expander("Read Full News 📖 "):
                st.write(article.text)
            st.write(f"[Original article here]({news_ls[i]['url']})")
        except Exception as err:
            print(err)
            