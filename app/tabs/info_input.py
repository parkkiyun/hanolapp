import streamlit as st

def render():
    st.header("정보 입력")
    
    # 기본 정보 입력
    st.text_input("성명", key="name")
    st.date_input("생년월일", key="birth_date")
    st.text_input("주소", key="address")
    st.text_input("연락처", key="contact")
    st.date_input("위임일", key="delegation_date")
