import streamlit as st

from pages.src.auth_pages import login_page, signup_page, start_page, profile_page
from pages.src.auth_pages import  reset_password_page, request_mail_page, change_avatar_page
from pages.src.auth_services import load_token, save_token, FILE_NAME


st.set_page_config(
    page_title="Auth",
    page_icon="lock",
)


if __name__ == '__main__':
    access_token, refresh_token = load_token(FILE_NAME)
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose action",
                                ["SignUp",
                                 "Login",
                                 "My Profile",
                                 "Resending email signup confirmation",
                                 "Reset password via email",
                                 "Change avatar",
                                 "Logout"]
                                )

    if page == "Login":
        if access_token:
            profile_page(access_token, refresh_token)
            access_token, refresh_token = load_token(FILE_NAME)
        else:
            access_token, refresh_token = login_page()

    elif page == "SignUp":
        if access_token:
            st.write("You are already in. Press Logout for SignUp")
        else:
            signup_page()

    elif page == "My Profile":
        if access_token:
            profile_page(access_token, refresh_token)
            access_token, refresh_token = load_token(FILE_NAME)
        else:
            start_page()

    elif page == "Resending email signup confirmation":
        if access_token:
            st.text("You already confirm email")
        else:
            request_mail_page()

    elif page == "Reset password via email":
        reset_password_page()

    elif page == "Change avatar":
        if access_token:
            change_avatar_page(access_token, refresh_token)
        else:
            start_page()

    if access_token:
        if st.button("Logout"):
            access_token, refresh_token = None, None
            save_token(access_token, refresh_token)
            st.experimental_rerun()

    save_token(access_token, refresh_token)
