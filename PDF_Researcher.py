import streamlit as st
from htmlTemplates import css


def main():
    st.set_page_config(page_title="Your own AI chat",
                       page_icon="👋")

    st.write(css, unsafe_allow_html=True)
    # author of banner: Afaque Umer
    st.image("static/banner.JPG")
    st.title("Welcome to PDF Researcher!")
    st.header("Sign up and enjoy AI-powered document research and analysis without language restrictions")


if __name__ == '__main__':
    main()
