import json
import streamlit as st
from pathlib import Path

class AuthManager:
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config" / "page_access.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.access_config = json.load(f)
        except FileNotFoundError:
            # 기본 설정 사용
            self.access_config = {
                "delegation_login": ["teacher"],
                "absence": ["teacher"],
                "field_trip_request": ["all"],
                "field_trip_report": ["all"],
                "write_delegation": ["all"]
            }

    def is_teacher_page(self, page_name):
        """페이지가 교사 전용인지 확인"""
        return self.access_config.get(page_name, []) == ["teacher"]

    def check_page_access(self, page_name):
        """페이지 접근 권한 확인"""
        if self.is_teacher_page(page_name):
            if not st.session_state.get("authenticated", False):
                st.error("이 페이지는 교사 로그인이 필요합니다.")
                st.switch_page("Home.py")
                st.stop()

    def authenticate(self, username, password):
        """사용자 인증"""
        if username == "teacher" and password == "1234":
            st.session_state["authenticated"] = True
            return True
        return False

    def logout(self):
        """로그아웃"""
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
    