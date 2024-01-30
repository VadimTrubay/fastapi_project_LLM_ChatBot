import streamlit as st

from pages.src.auth_services import login, signup
from pages.src.auth_services import get_user_info, set_new_pass, set_avatar
from pages.src.auth_services import reset_password, request_email

IMG_TYPE = ['png', 'jpg', 'jpeg', 'gif', 'svg']


def login_page():
    """
    The login_page function is the first page of the app. It allows users to login with their Spotify credentials.
    If they are successful, it returns a tuple containing an access token and refresh token for use in other functions.

    :return: A tuple of access_token and refresh_token
    :doc-author: Trelent
    """
    acc_token, ref_token = None, None
    st.title("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = login(username, password)
        if type(res) == tuple:
            acc_token, ref_token = res
            st.success("Success.")
            # profile_page(acc_token, ref_token)
            return acc_token, ref_token
        elif type(res) == str:
            st.text("Email is not confirmed.")
        else:
            st.error("Wrong username or password")
    return None, None


def change_avatar_page(acc_token, ref_token):
    """
    The change_avatar_page function is used to change the avatar of a user.
    It takes two parameters: acc_token and ref_token.
    The function first checks if there is an image uploaded by the user, then it processes it using set_avatar()
     function from api.py file.

    :param acc_token: Access the user's account
    :param ref_token: Get a new access token
    :return: The set_avatar function
    :doc-author: Trelent
    """
    new_avatar = st.file_uploader("Upload your image here and click on 'Process'", type=IMG_TYPE)
    if new_avatar:
        if st.button("Process"):
            with st.spinner("Processing"):
                res = set_avatar(acc_token, new_avatar.getvalue())
                if res.get("avatar"):
                    st.success("Avatar update successfully.")
                else:
                    st.error(f"Error: {res}")


def request_mail_page():
    """
    The request_mail_page function is used to resend the email signup confirmation.
    The user enters their email address and clicks the &quot;Request Email&quot; button.
    If successful, a success message will appear.

    :return: A success message if the email request is successful
    :doc-author: Trelent
    """
    st.title("Resending email signup confirmation")
    email_reset = st.text_input("Email request")
    if st.button("Request email"):
        request_email(email_reset)
        st.success(f"Success.  Check email: {email_reset} and verify")


def reset_password_page():
    """
    The reset_password_page function is used to reset a user's password.
        The function takes no arguments and returns nothing.

    :return: A string
    :doc-author: Trelent
    """
    st.title("Reset password via email")
    email_reset = st.text_input("Email for reset password")
    if st.button("Reset password"):
        print(reset_password(email_reset))
        st.success(f"Success.  Check email: {email_reset}")
    pass_token = st.text_input("Paste token from email")
    password = st.text_input("New password", type="password")
    password_confirm = st.text_input("Confirm new password", type="password")
    if st.button("Reset confirm"):
        if password == password_confirm:
            res = set_new_pass(pass_token, password, password_confirm)
            if res:
                st.success(f"{res}")
            else:
                st.error(f"Something wrong.")
        else:
            st.error("Password not match")


def start_page():
    """
    The start_page function is used to display the title of the page.

    :return: The start page of the app
    :doc-author: Trelent
    """
    st.title("Login for use all features")


def profile_page(acc_token, ref_token):
    """
    The profile_page function is used to display the user's profile information.
    It takes in two parameters: acc_token and ref_token, which are both strings.
    The function uses the get_user_info function to retrieve a dictionary of user info from Spotify's API.
    If this succeeds, it displays the username, email address and avatar image for that user.

    :param acc_token: Get the user information
    :param ref_token: Get a new access token
    :return: The user information
    :doc-author: Trelent
    """
    st.title("My profile")
    user_info = get_user_info(acc_token, ref_token)
    if user_info:
        st.write(f"Username: {user_info['username']}")
        st.write(f"Email: {user_info['email']}")
        st.image(f"{user_info['avatar']}")
    else:
        st.error("Unable connect")


def signup_page():
    """
    The signup_page function is used to create a new user account.
    It takes no arguments and returns nothing.


    :return: A dictionary with the id and username of the user
    :doc-author: Trelent
    """
    st.title("SignUp")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm password", type="password")
    if st.button("SignUp confirm"):
        if password == password_confirm:
            res = signup(username, email, password)
            if res.get("id"):
                st.success(f"Success. Check email: {email} and verify")
            else:
                st.error(f"{res['detail']}")
        else:
            st.error("Password not match")
